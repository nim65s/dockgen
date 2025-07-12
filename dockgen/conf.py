"""Configuration for dockgen."""

from argparse import ArgumentParser, Namespace
from logging import basicConfig, getLogger
from os import environ
from pathlib import Path
from subprocess import check_output
from tempfile import mkdtemp


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Generate fresh docker images", prog="dockgen")
    parser.add_argument(
        "-f",
        "--file",
        default=Path("dockgen.toml"),
        type=Path,
        help="Configuration file",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=int(environ.get("QUIET", 0)),
        help="decrement verbosity level",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=int(environ.get("VERBOSITY", 0)),
        help="increment verbosity level",
    )
    parser.add_argument(
        "--token",
        default=environ.get("GITHUB_TOKEN", ""),
        help="Forge API token. Can be specified via `GITHUB_TOKEN` or `GITHUB_TOKEN_CMD`",
    )
    parser.add_argument(
        "--work-dir",
        default=mkdtemp(),
        type=Path,
    )
    parser.add_argument(
        "--from",
        default="ubuntu:24.04",
        help="Base docker image",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=Path("Dockerfile"),
        type=Path,
        help="Output Dockerfile",
    )
    parser.add_argument(
        "--jobs",
        default=4,
        type=int,
        help="Number of build jobs",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build the docker image",
    )
    parser.add_argument(
        "--name",
        default="dockgen",
        help="Docker image name",
    )
    return parser


def get_conf(parser: ArgumentParser) -> Namespace:
    logger = getLogger("dockgen.conf")
    args = parser.parse_args()
    basicConfig(level=30 - 10 * args.verbose + 10 * args.quiet)

    if not args.token and "GITHUB_TOKEN_CMD" in environ:
        cmd = environ["GITHUB_TOKEN_CMD"].split()
        logger.debug("Calling '%s' to get token", cmd)
        args.token = check_output(cmd, text=True).strip()

    return args
