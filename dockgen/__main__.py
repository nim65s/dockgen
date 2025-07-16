"""Generate fresh docker images."""

from argparse import Namespace
from logging import getLogger
from subprocess import check_call

from tomllib import load
from jinja2 import Environment, PackageLoader, select_autoescape

from .conf import get_parser, get_conf
from .project import Project

logger = getLogger("dockgen")

GENERAL_APT_DEPS = [
    "build-essential",
    "cmake",
    "git",
    "libpython3-dev",
    "python-is-python3",
]


class Dockgen:
    def __init__(self, args: Namespace):
        self.args = args
        self.projects = {}
        self.projects_order = []
        with args.file.open("rb") as f:
            for k, v in load(f).items():
                self.projects[k] = Project(dockgen=self, name=k, **v)
                self.projects_order.append(k)

        env = Environment(
            loader=PackageLoader("dockgen"), autoescape=select_autoescape()
        )
        layer = env.get_template("layer.Dockerfile")

        layers = [
            layer.render(args=args, project=self.projects[project])
            for project in self.projects_order
        ]

        main = env.get_template("main.Dockerfile")

        apt_deps = " \\\n    ".join(
            sorted(
                {
                    *GENERAL_APT_DEPS,
                    *(d for p in self.projects.values() for d in p.apt_deps),
                }
            )
        )

        with args.output.open("w") as out:
            print(main.render(args=args, apt_deps=apt_deps), file=out)
            print(file=out)
            for layer in layers:
                print(layer, file=out)
                print(file=out)

        if args.build:
            logger.info("Building image %s", args.name)
            check_call(
                ["docker", "build", "-t", args.name, "-f", str(args.output), "."]
            )


def main():
    parser = get_parser()
    Dockgen(get_conf(parser))


if __name__ == "__main__":
    main()
