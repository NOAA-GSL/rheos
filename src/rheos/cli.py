import json
import sys
from argparse import ArgumentParser, HelpFormatter, Namespace, _ArgumentGroup
from collections.abc import Callable
from pathlib import Path
from typing import Any, NoReturn

from uwtools.api.logging import use_uwtools_logger

from rheos.api import config
from rheos.util import pkgname, resource

# Mapping of modes to actions, and of actions to functions plus their arguments (names mapped to
# ArgumentParser.add_argument() keyword arguments, where names starting with "-" are optional and
# others are required):

MODES: dict[str, dict[str, tuple[Callable[..., None], dict[str, dict[str, Any]]]]] = {
    "config": {
        "cat": (
            lambda key_path: print(config.read(key_path.split("/")), end=""),
            {
                "key_path": {
                    "help": "Slash-separated path to config resource",
                    "metavar": "KEY_PATH",
                }
            },
        ),
        "compose": (
            lambda configs, realize: print(config.compose(configs, realize=realize)),
            {
                "--realize": {"action": "store_true", "help": "Realize the composed config"},
                "configs": {
                    "help": "Config files, or config resource key paths, to compose",
                    "metavar": "CONFIG",
                    "nargs": "+",
                },
            },
        ),
        "ls": (
            lambda: print("".join(f"{x}\n" for x in config.catalog()), end=""),
            {},
        ),
    },
}

# Public


def main() -> None:
    args = _parse_args(sys.argv)
    use_uwtools_logger(verbose=args.debug)
    function, arguments = MODES[args.mode][args.action]
    dests = [name.lstrip("-") for name in arguments]
    function(**{dest: getattr(args, dest) for dest in dests})


# Private


class _Parser(ArgumentParser):
    """
    An ArgumentParser listing available choices (modes or actions) in its help and errors.
    """

    def __init__(self, *args: Any, choices: list[str], label: str, **kwargs: Any) -> None:  # noqa: ANN401
        kwargs.setdefault("add_help", False)
        kwargs.setdefault("formatter_class", _formatter)
        super().__init__(*args, **kwargs)
        self.choices = choices
        self.label = label

    def error(self, message: str) -> NoReturn:
        self.print_help(sys.stderr)
        self.exit(2, f"\n{self.prog}: error: {message}\n")

    def format_help(self) -> str:
        lines = [f"Available {self.label}:", *[f"  {x}" for x in self.choices], ""]
        return super().format_help() + "\n" + "\n".join(lines)


def _add_common_args(parser: ArgumentParser, argv0: str, *, debug: bool = False) -> _ArgumentGroup:
    optional = parser.add_argument_group("Optional arguments")
    if debug:
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
        version=f"{Path(argv0).name} {_version()}",
    )
    return optional


def _formatter(prog: str) -> HelpFormatter:
    return HelpFormatter(prog, max_help_position=6)


def _parse_args(argv: list[str]) -> Namespace:
    parser = _Parser(description=pkgname, choices=list(MODES), label="modes")
    _add_common_args(parser, argv[0])
    modes = parser.add_subparsers(dest="mode", metavar="MODE", parser_class=_Parser, required=True)
    for mode, actions in MODES.items():
        mode_parser = modes.add_parser(mode, choices=list(actions), label="actions")
        _add_common_args(mode_parser, argv[0])
        actions_subparsers = mode_parser.add_subparsers(
            dest="action", metavar="ACTION", parser_class=ArgumentParser, required=True
        )
        for action, (_, arguments) in actions.items():
            action_parser = actions_subparsers.add_parser(
                action, add_help=False, formatter_class=_formatter
            )
            positionals = {k: v for k, v in arguments.items() if not k.startswith("-")}
            if positionals:
                required = action_parser.add_argument_group("Required arguments")
                for name, kwargs in positionals.items():
                    required.add_argument(name, **kwargs)
            optional = _add_common_args(action_parser, argv[0], debug=True)
            for name, kwargs in arguments.items():
                if name.startswith("-"):
                    optional.add_argument(name, **kwargs)
    args = argv[1:]
    if not args or (len(args) == 1 and args[0] in MODES):
        args.append("--help")
    return parser.parse_args(args)


def _version() -> str:
    info = json.loads(resource("info.json"))
    return "version %s" % info["version"]
