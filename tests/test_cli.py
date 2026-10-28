import sys
from argparse import Namespace
from importlib import import_module

import pytest

from rheos import cli
from rheos.util import resource


@pytest.mark.parametrize(
    ("action", "extra", "expected"),
    [
        ("compose", {}, "rheos.api.config.compose() called"),
        ("ls", {}, "platform/ursa.yaml"),
        (
            "show",
            {"key_path": "platform/ursa.yaml"},
            resource("config/platform/ursa.yaml"),
        ),
    ],
)
def test_main(action, capsys, expected, extra, mocker):
    namespace = Namespace(action=action, debug=True, mode="config", **extra)
    parse_args = mocker.patch.object(cli, "_parse_args", return_value=namespace)
    use_logger = mocker.patch.object(cli, "use_uwtools_logger")
    mocker.patch.object(sys, "argv", ["rheos", "config", action, "-d"])
    cli.main()
    parse_args.assert_called_once_with(["rheos", "config", action, "-d"])
    use_logger.assert_called_once_with(verbose=True)
    assert expected in capsys.readouterr().out


@pytest.mark.parametrize(("mode", "actions"), cli.MODES.items())
def test_modes(mode, actions):
    module = import_module(f"rheos.api.{mode}")
    for function, _ in actions.values():
        assert callable(getattr(module, function))


def _patch_version(mocker):
    mocker.patch.object(cli, "_version", return_value="version 1.2.3 build 4")


@pytest.mark.parametrize(
    ("action", "positionals"), [("compose", []), ("ls", []), ("show", ["a/b.yaml"])]
)
@pytest.mark.parametrize("debug", [[], ["-d"], ["--debug"]])
def test__parse_args(action, debug, mocker, positionals):
    _patch_version(mocker)
    args = cli._parse_args(["rheos", "config", action, *positionals, *debug])
    assert args.mode == "config"
    assert args.action == action
    assert args.debug is bool(debug)
    if positionals:
        assert args.key_path == positionals[0]


@pytest.mark.parametrize("code", [2])
def test__parse_args_missing_positional(capsys, code, mocker):
    _patch_version(mocker)
    with pytest.raises(SystemExit) as e:
        cli._parse_args(["rheos", "config", "show"])
    assert e.value.code == code
    assert "KEY_PATH" in capsys.readouterr().err


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
        ["config", "ls", "-h"],
        ["config", "ls", "--version"],
    ],
)
def test__parse_args_exit(argv, mocker):
    _patch_version(mocker)
    with pytest.raises(SystemExit) as e:
        cli._parse_args(["rheos", *argv])
    assert e.value.code == 0


def test__version(mocker):
    mocker.patch.object(cli, "resource", return_value='{"version": "1.2.3", "buildnum": "4"}')
    assert cli._version() == "version 1.2.3"
