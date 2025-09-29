from pathlib import Path
from subprocess import check_output
from sys import executable
from tempfile import mktemp
from unittest import TestCase

from dockgen import Dockgen
from dockgen.conf import get_conf, get_parser


class DockgenTest(TestCase):
    def test_eigenpy(self):
        args = get_conf(get_parser())
        args.file = Path(__file__).parent / "eigenpy.toml"
        args.output = Path(mktemp())
        Dockgen(args)
        output = args.output.read_text()
        self.assertIn(
            "ADD . .",
            output,
        )

    def test_example_robot_data(self):
        args = get_conf(get_parser())
        args.file = Path(__file__).parent / "example-robot-data.toml"
        args.output = Path(mktemp())
        Dockgen(args)
        output = args.output.read_text()
        self.assertIn(
            "          -DBUILD_PYTHON_INTERFACE=OFF \\",
            output,
        )

    def test_online_eigenpy(self):
        args = get_conf(get_parser())
        args.file = Path(__file__).parent / "online-eigenpy.toml"
        args.output = Path(mktemp())
        Dockgen(args)
        output = args.output.read_text()
        self.assertIn(
            "ADD https://api.github.com/repos/jrl-umi3218/jrl-cmakemodules/tarball/v",
            output,
        )

    def test_jrl_cmakemodules(self):
        args = get_conf(get_parser())
        args.file = Path(__file__).parent / "jrl-cmakemodules.toml"
        args.output = Path(mktemp())
        args.build = True
        args.name = "dockgen-test"
        Dockgen(args)
        output = args.output.read_text()
        self.assertIn(
            "ADD https://api.github.com/repos/jrl-umi3218/jrl-cmakemodules/tarball/v",
            output,
        )
        docker = check_output(
            [
                "docker",
                "run",
                "--rm",
                args.name,
                "cat",
                "/usr/local/lib/cmake/jrl-cmakemodules/jrl-cmakemodulesConfig.cmake",
            ],
            text=True,
        )
        self.assertIn("/jrl-cmakemodulesTargets.cmake", docker)

    def test_wrong(self):
        args = get_conf(get_parser())
        args.file = Path(__file__).parent / "wrong.toml"
        with self.assertRaises(AttributeError):
            Dockgen(args)

    def test_help(self):
        exe = [executable]
        try:
            import coverage  # noqa: F401

            exe = ["coverage", "run"]
        except ImportError:  # pragma: no cover
            pass
        output = check_output([*exe, "-m", "dockgen", "-h"], text=True)
        self.assertIn("Generate fresh docker images", output)
