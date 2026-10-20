import sys
from argparse import Namespace

import pytest

from rheos import cli


def test_main(mocker):
    parse_args = mocker.patch.object(cli, "_parse_args", return_value=Namespace(debug=True))
    use_logger = mocker.patch.object(cli, "use_uwtools_logger")
    mocker.patch.object(sys, "argv", ["rheos", "-d"])
    cli.main()
    parse_args.assert_called_once_with(["rheos", "-d"])
    use_logger.assert_called_once_with(verbose=True)


def _patch_version(mocker):
    mocker.patch.object(cli, "version", return_value="version 1.2.3 build 4")


def test__parse_args_config(mocker):
    _patch_version(mocker)
    args = cli._parse_args(["rheos", "-c", "config.yaml"])
    assert str(args.config) == "config.yaml"
    assert args.debug is False


def test__parse_args_debug(mocker):
    _patch_version(mocker)
    args = cli._parse_args(["rheos", "--debug"])
    assert args.debug is True


@pytest.mark.parametrize("flag", ["-h", "--help", "-v", "--version"])
def test__parse_args_exit(mocker, flag):
    _patch_version(mocker)
    with pytest.raises(SystemExit) as e:
        cli._parse_args(["rheos", flag])
    assert e.value.code == 0
