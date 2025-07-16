"""Definition of a software forge."""

from argparse import Namespace
from enum import StrEnum
from logging import getLogger
from pathlib import Path
from urllib.parse import urlparse
from shutil import unpack_archive
# from subprocess import check_call

import httpx

logger = getLogger("dockgen.forge")


class ForgeType(StrEnum):
    GitHub = "github:"
    HTTP = "http"
    Dot = "."
    # Git = "git"


class Forge:
    def __init__(
        self, args: Namespace, forge_type: ForgeType, url: str, name: str | None
    ):
        self.args = args
        self.forge_type = forge_type
        self.url = url
        self.headers = {}
        self.org = None
        self.name = name
        self.dir = args.work_dir / self.name
        self.slug = (
            "dot"
            if self.forge_type == ForgeType.Dot
            else str(self.forge_type).removesuffix(":")
        )
        getattr(self, f"init_{self.slug}")()

    def init_github(self):
        if "/" not in self.url:
            self.url = f"{self.url}/{self.name}"
        self.org, self.name = self.url.removeprefix("github:").split("/")[:2]
        self.headers = {"Accept": "application/vnd.github+json"}
        if self.args.token:
            self.headers["Authorization"] = f"Bearer {self.args.token}"
        self.dir.mkdir(parents=True, exist_ok=True)

        self.api_url = f"https://api.github.com/repos/{self.org}/{self.name}"
        latest = httpx.get(
            f"{self.api_url}/releases/latest", headers=self.headers
        ).json()
        self.version = latest["tag_name"]
        self.tarball = latest["tarball_url"]

    def init_http(self):
        if not self.name:
            err = f"name must be set for {self.url}"
            raise AttributeError(err)
        self.tarball = self.url
        if self.dir.exists():
            logger.info("%s already exists, skipping download", self.dir)
        else:
            logger.info("downloading %s to %s", self.url, self.args.work_dir)
            self.args.work_dir.mkdir(parents=True)
            filename = Path(urlparse(self.url).path).name
            with (self.args.work_dir / filename).open("wb") as f:
                with httpx.stream("GET", self.url) as r:
                    for data in r.iter_bytes():
                        f.write(data)
            logger.info("extracting %s to %s", filename, self.dir)
            unpack_archive(self.args.work_dir / filename, self.dir)

    def init_dot(self):
        self.version = None
        self.tarball = None

    # def init_git(self):
    #     self.name = self.name or self.url.removesuffix(".git").split("/")[-1]
    #     self.dir = self.args.work_dir / self.name
    #     if self.dir.exists():
    #         logger.info("%s already exists, skipping clone", self.dir)
    #     else:
    #         logger.info("cloning %s to %s", self.url, self.args.work_dir)
    #         check_call(["git", "clone", self.url], cwd=self.args.work_dir)
    #     self.tarbal = ???

    def get_file(self, path: Path) -> Path | None:
        method = f"get_file_{self.slug}"
        if hasattr(self, method):
            return getattr(self, method)(path)
        path = self.dir / path
        if path.exists():
            return path
        return None

    def get_file_github(self, path: Path) -> Path | None:
        url = f"https://api.github.com/repos/{self.org}/{self.name}"
        content = httpx.get(f"{url}/contents/{path}", headers=self.headers)
        if content.status_code == 200:
            download_url = content.json()["download_url"]
            content = httpx.get(download_url, headers=self.headers)
            if content.status_code == 200:
                path = self.dir / path
                path.write_text(content.text)
                return path
        return None
