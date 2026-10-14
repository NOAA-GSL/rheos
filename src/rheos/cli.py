import logging
import sys
import traceback
from argparse import ArgumentParser, ArgumentTypeError, HelpFormatter, Namespace
from pathlib import Path

from iotaa import tasknames
from uwtools.api.config import YAMLConfig, get_yaml_config, validate
from uwtools.api.logging import use_uwtools_logger
from wxvx import workflow
from wxvx.config import Config
from wxvx.net import initialize_session
from wxvx.util import (
    WXVXError,
    fail,
    finalize_pool,
    initialize_pool,
    pkgname,
    resource_path,
    version,
)

# Public


def main() -> None:
    args = _parse_args(sys.argv)
    use_uwtools_logger(verbose=args.debug)


# Private


def _parse_args(argv: list[str]) -> Namespace:
    parser = ArgumentParser(
        description=pkgname,
        add_help=False,
        formatter_class=lambda prog: HelpFormatter(prog, max_help_position=6),
    )
    required = parser.add_argument_group("Required arguments")
    required.add_argument(
        "-c",
        "--config",
        help="Configuration file",
        metavar="FILE",
        type=Path,
    )
    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Log all messages",
    )
    optional.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show help and exit",
    )
    optional.add_argument(
        "-v",
        "--version",
        action="version",
        help="Show version and exit",
        version=f"{Path(argv[0]).name} {version()}",
    )
    return parser.parse_args(argv[1:])
