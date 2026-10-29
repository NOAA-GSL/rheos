import sys
from argparse import Namespace
from importlib import import_module
from unittest.mock import patch

from pytest import fixture, mark, raises

from rheos import cli

# Fixtures


@fixture
def version():
    with patch.object(cli, "_version", return_value="version 1.2.3 build 4"):
        yield


# Tests


@mark.parametrize(
    ("action", "extra", "expected"),
    [
        ("compose", {"configs": ["a.yaml", "x/y/b.yaml"], "realize": False}, "c: 2"),
        ("ls", {}, "a.yaml\nx/y/b.yaml\n"),
        ("show", {"key_path": "x/y/b.yaml"}, "c: 2\n"),
    ],
)
@mark.usefixtures("config_root")
def test_main(action, capsys, expected, extra):
    argv = ["rheos", "config", action, "-d"]
    namespace = Namespace(action=action, debug=True, mode="config", **extra)
    with (
        patch.object(cli, "_parse_args", return_value=namespace) as parse_args,
        patch.object(cli, "use_uwtools_logger") as use_logger,
        patch.object(sys, "argv", argv),
    ):
        cli.main()
    parse_args.assert_called_once_with(argv)
    use_logger.assert_called_once_with(verbose=True)
    assert expected in capsys.readouterr().out


@mark.parametrize(("mode", "actions"), cli.MODES.items())
def test_modes(mode, actions):
    module = import_module(f"rheos.api.{mode}")
    for function, _ in actions.values():
        assert callable(getattr(module, function))


@mark.parametrize(
    ("action", "argv", "expected"),
    [
        ("compose", ["a.yaml"], {"configs": ["a.yaml"], "realize": False}),
        ("compose", ["a.yaml", "b.yaml"], {"configs": ["a.yaml", "b.yaml"], "realize": False}),
        ("compose", ["--realize", "a.yaml"], {"configs": ["a.yaml"], "realize": True}),
        ("ls", [], {}),
        ("show", ["a/b.yaml"], {"key_path": "a/b.yaml"}),
    ],
)
@mark.parametrize("debug", [[], ["-d"], ["--debug"]])
@mark.usefixtures("version")
def test__parse_args(action, argv, debug, expected):
    args = cli._parse_args(["rheos", "config", action, *argv, *debug])
    assert args.mode == "config"
    assert args.action == action
    assert args.debug is bool(debug)
    for k, v in expected.items():
        assert getattr(args, k) == v


@mark.parametrize(("action", "metavar"), [("compose", "CONFIG"), ("show", "KEY_PATH")])
@mark.parametrize("code", [2])
@mark.usefixtures("version")
def test__parse_args_missing_positional(action, capsys, code, metavar):
    with raises(SystemExit) as e:
        cli._parse_args(["rheos", "config", action])
    assert e.value.code == code
    assert metavar in capsys.readouterr().err


@mark.parametrize(
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
@mark.usefixtures("version")
def test__parse_args_help(argv, capsys, code, expected):
    with raises(SystemExit) as e:
        cli._parse_args(["rheos", *argv])
    assert e.value.code == code
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert expected in output
    assert output.index("usage:") < output.index(expected)
    choices = cli.MODES["config"] if expected == "Available actions:" else list(cli.MODES)
    for choice in choices:
        assert f"  {choice}\n" in output


@mark.parametrize(
    "argv",
    [
        ["-v"],
        ["--version"],
        ["config", "-v"],
        ["config", "ls", "-h"],
        ["config", "ls", "--version"],
    ],
)
@mark.usefixtures("version")
def test__parse_args_exit(argv):
    with raises(SystemExit) as e:
        cli._parse_args(["rheos", *argv])
    assert e.value.code == 0


def test__version():
    with patch.object(cli, "resource", return_value='{"version": "1.2.3", "buildnum": "4"}'):
        assert cli._version() == "version 1.2.3"
