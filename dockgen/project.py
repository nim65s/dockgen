"""Definition of a project to build."""

from enum import StrEnum
from pathlib import Path
from tomllib import load
from typing import TYPE_CHECKING

from .forge import Forge, ForgeType


if TYPE_CHECKING:  # pragma: no cover
    from .__main__ import Dockgen


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
        dockgen: "Dockgen",
        name: str,
        url: str,
        org: str | None = None,
        version: str | None = None,
        tarball: str | None = None,
        build_systems: list[str] | None = None,
        apt_deps: list[str] | None = None,
        src_deps: list[str] | None = None,
    ):
        self.dockgen = dockgen
        self.name = name
        self.url = url
        for forge_type in ForgeType:
            if self.url.startswith(forge_type):
                self.forge = Forge(dockgen.args, forge_type, url, name)
                break
        else:
            err = f"Project {name} at {url} has an unknown forge"
            raise AttributeError(err)

        self.org = org or self.forge.org
        self.version = version or self.forge.version
        self.tarball = tarball or self.forge.tarball
        self.build_systems = [BuildSystem[b] for b in (build_systems or self.detect())]
        self.apt_deps = set(apt_deps or [])
        self.src_deps = set(src_deps or [])

        if self.url != ".":
            if upstream_dockgen := self.forge.get_file("dockgen.toml"):
                self.upstream(upstream_dockgen)

    def detect(self) -> list[str]:
        """
        Detect build systems
        """
        return [
            build_system.name
            for build_system in BuildSystem
            if self.forge.get_file(build_system) is not None
        ]

    def upstream(self, upstream_dockgen: Path):
        """
        Process data from upstream dockgen.toml
        """
        with upstream_dockgen.open("rb") as f:
            for name, conf in load(f).items():
                if name == self.name:
                    tgt = self
                elif name in self.dockgen.projects:
                    tgt = self.dockgen.projects[name]
                else:
                    self.dockgen.projects[name] = Project(
                        dockgen=self.dockgen, name=name, **conf
                    )
                    self.dockgen.projects_order.append(name)
                    continue

                for k, v in conf.items():
                    match k:
                        case "apt_deps":
                            tgt.apt_deps |= set(v)
                        case "src_deps":
                            tgt.src_deps |= set(v)
