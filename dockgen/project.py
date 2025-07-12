"""Definition of a project to build."""

from argparse import Namespace
from enum import StrEnum

from .forge import Forge, ForgeType


class BuildSystem(StrEnum):
    CMake = "CMakeLists.txt"


class Project:
    url: str
    tarball: str
    org: str | None
    name: str
    version: str | None
    forge: Forge
    build_systems: [BuildSystem]
    apt_deps: set[str]
    src_deps: set[str]

    def __init__(
        self,
        args: Namespace,
        name: str,
        url: str,
        org: str | None = None,
        version: str | None = None,
        tarball: str | None = None,
        build_systems: list[str] | None = None,
        apt_deps: list[str] | None = None,
        src_deps: list[str] | None = None,
    ):
        self.name = name
        self.url = url
        for forge_type in ForgeType:
            if self.url.startswith(forge_type):
                self.forge = Forge(args, forge_type, url, name)
                break
        else:
            err = f"Project {name} at {url} has an unknown forge"
            raise RuntimeError(err)

        self.org = org or self.forge.org
        self.version = version or self.forge.version
        self.tarball = tarball or self.forge.tarball
        self.build_systems = [BuildSystem[b] for b in (build_systems or ["CMake"])]
        self.apt_deps = set(apt_deps or [])
        self.src_deps = set(src_deps or [])

        # TODO
        # upstream_dockgen = self.forge.get_file("dockgen.toml")
