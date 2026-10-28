from pathlib import Path

import pytest

from rheos.api import config
from rheos.util import resource_path


def test_compose(capsys):
    config.compose()
    assert "rheos.api.config.compose() called" in capsys.readouterr().out


def test_ls():
    assert config.ls() == ["base.yaml", "platform/ursa.yaml", "workflow/rocoto.yaml"]


def test_ls_to_stdout(capsys):
    config.ls_to_stdout()
    assert capsys.readouterr().out == "base.yaml\nplatform/ursa.yaml\nworkflow/rocoto.yaml\n"


@pytest.mark.parametrize("key_path", [["base.yaml"], ["platform", "ursa.yaml"]])
def test_show(key_path):
    expected = resource_path(Path("config", *key_path)).read_text()
    assert config.show(key_path) == expected


@pytest.mark.parametrize("key_path", ["base.yaml", "platform/ursa.yaml"])
def test_show_to_stdout(capsys, key_path):
    config.show_to_stdout(key_path)
    assert capsys.readouterr().out == resource_path(Path("config", key_path)).read_text()


def test__walk(tmp_path):
    for relpath in [
        "__init__.py",
        "__pycache__/x.pyc",
        "a/__init__.py",
        "a/b/c/d.yaml",
        "a/e.yaml",
        "f.yaml",
    ]:
        path = tmp_path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    assert sorted(config._walk(tmp_path, [])) == ["a/b/c/d.yaml", "a/e.yaml", "f.yaml"]
