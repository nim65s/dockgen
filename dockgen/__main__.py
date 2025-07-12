"""Generate fresh docker images."""

from logging import getLogger
from subprocess import check_call

from tomllib import load
from jinja2 import Environment, PackageLoader, select_autoescape

from .conf import get_parser, get_conf
from .project import Project

logger = getLogger("dockgen")


def main():
    parser = get_parser()
    args = get_conf(parser)

    env = Environment(loader=PackageLoader("dockgen"), autoescape=select_autoescape())
    layers = []
    apt_deps = set(
        [
            "build-essential",
            "cmake",
            "git",
            "libpython3-dev",
            "python-is-python3",
        ]
    )
    layer = env.get_template("layer.Dockerfile")
    with args.file.open("rb") as f:
        for k, v in load(f).items():
            project = Project(args=args, name=k, **v)
            apt_deps |= project.apt_deps
            layers.append(layer.render(args=args, project=project))

    main = env.get_template("main.Dockerfile")

    apt_deps = " \\\n    ".join(sorted(apt_deps))

    with args.output.open("w") as out:
        print(main.render(args=args, apt_deps=apt_deps), file=out)
        print(file=out)
        for layer in layers:
            print(layer, file=out)
            print(file=out)

    if args.build:
        logger.info("Building image %s", args.name)
        check_call(["docker", "build", "-t", args.name, "-f", str(args.output), "."])


if __name__ == "__main__":
    main()
