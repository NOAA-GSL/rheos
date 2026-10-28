import sys
from argparse import ArgumentParser, HelpFormatter, Namespace
from importlib import import_module
from pathlib import Path
from typing import Any, NoReturn

from uwtools.api.logging import use_uwtools_logger

from rheos.util import pkgname, version

# Mapping of modes (rheos.api modules) to actions, and of actions to functions in those modules
# plus their positional arguments (names mapped to help strings):

MODES: dict[str, dict[str, tuple[str, dict[str, str]]]] = {
    "config": {
        "compose": ("compose", {}),
        "ls": ("ls_to_stdout", {}),
        "show": ("show_to_stdout", {"key_path": "Slash-separated path to config resource"}),
    },
}

# Public


def main() -> None:
    args = _parse_args(sys.argv)
    use_uwtools_logger(verbose=args.debug)
    module = import_module(f"{pkgname}.api.{args.mode}")
    function, positionals = MODES[args.mode][args.action]
    getattr(module, function)(**{name: getattr(args, name) for name in positionals})


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


def _add_common_args(parser: ArgumentParser, argv0: str, debug: bool = False) -> None:  # noqa: FBT001,FBT002
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
        version=f"{Path(argv0).name} {version()}",
    )


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
        for action, (_, positionals) in actions.items():
            action_parser = actions_subparsers.add_parser(
                action, add_help=False, formatter_class=_formatter
            )
            if positionals:
                required = action_parser.add_argument_group("Required arguments")
                for name, helpmsg in positionals.items():
                    required.add_argument(name, help=helpmsg, metavar=name.upper())
            _add_common_args(action_parser, argv[0], debug=True)
    args = argv[1:]
    if not args or (len(args) == 1 and args[0] in MODES):
        args.append("--help")
    return parser.parse_args(args)
