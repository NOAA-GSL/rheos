import sys
from argparse import Namespace
from importlib import import_module

import pytest

from rheos import cli


@pytest.mark.parametrize("action", ["compose", "extract", "list"])
def test_main(action, capsys, mocker):
    parse_args = mocker.patch.object(
        cli, "_parse_args", return_value=Namespace(action=action, debug=True, mode="config")
    )
    use_logger = mocker.patch.object(cli, "use_uwtools_logger")
    mocker.patch.object(sys, "argv", ["rheos", "config", action, "-d"])
    cli.main()
    parse_args.assert_called_once_with(["rheos", "config", action, "-d"])
    use_logger.assert_called_once_with(verbose=True)
    assert f"rheos.api.config.{action}() called" in capsys.readouterr().out


@pytest.mark.parametrize(("mode", "actions"), cli.MODES.items())
def test_modes(mode, actions):
    module = import_module(f"rheos.api.{mode}")
    for action in actions:
        assert callable(getattr(module, action))


def _patch_version(mocker):
    mocker.patch.object(cli, "version", return_value="version 1.2.3 build 4")


@pytest.mark.parametrize("action", ["compose", "extract", "list"])
@pytest.mark.parametrize("debug", [[], ["-d"], ["--debug"]])
def test__parse_args(action, debug, mocker):
    _patch_version(mocker)
    args = cli._parse_args(["rheos", "config", action, *debug])
    assert args.mode == "config"
    assert args.action == action
    assert args.debug is bool(debug)


@pytest.mark.parametrize(
    ("argv", "code", "expected"),
    [
        ([], 0, "Available modes:"),
        (["-h"], 0, "Available modes:"),
        (["--help"], 0, "Available modes:"),
        (["foo"], 2, "Available modes:"),
        (["config"], 0, "Available actions:"),
        (["config", "-h"], 0, "Available actions:"),
        (["config", "--help"], 0, "Available actions:"),
        (["config", "foo"], 2, "Available actions:"),
    ],
)
def test__parse_args_help(argv, capsys, code, expected, mocker):
    _patch_version(mocker)
    with pytest.raises(SystemExit) as e:
        cli._parse_args(["rheos", *argv])
    assert e.value.code == code
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert expected in output
    assert output.index("usage:") < output.index(expected)
    choices = cli.MODES["config"] if expected == "Available actions:" else list(cli.MODES)
    for choice in choices:
        assert f"  {choice}\n" in output


@pytest.mark.parametrize(
    "argv",
    [
        ["-v"],
        ["--version"],
        ["config", "-v"],
        ["config", "list", "-h"],
        ["config", "list", "--version"],
    ],
)
def test__parse_args_exit(argv, mocker):
    _patch_version(mocker)
    with pytest.raises(SystemExit) as e:
        cli._parse_args(["rheos", *argv])
    assert e.value.code == 0
