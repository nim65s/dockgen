from pathlib import Path
from tempfile import mktemp
from unittest import TestCase

from dockgen import main
from dockgen.conf import get_parser


class DockgenTest(TestCase):
    def test_eigenpy(self):
        args = get_parser().parse_args()
        args.file = Path(__file__).parent / "eigenpy.toml"
        args.output = Path(mktemp())
        main(args)
        output = args.output.read_text()
        self.assertIn(
            "ADD https://api.github.com/repos/jrl-umi3218/jrl-cmakemodules/tarball/v",
            output,
        )
