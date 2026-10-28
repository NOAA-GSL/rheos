from pathlib import Path

import pytest

from rheos.api import config
from rheos.util import resource_path


def test_catalog():
    assert config.catalog() == ["base.yaml", "platform/ursa.yaml", "workflow/rocoto.yaml"]


def test_compose(capsys):
    config.compose()
    assert "rheos.api.config.compose() called" in capsys.readouterr().out


@pytest.mark.parametrize("key_path", [["base.yaml"], ["platform", "ursa.yaml"]])
def test_extract(key_path):
    expected = resource_path(Path("config", *key_path)).read_text()
    assert config.extract(key_path) == expected


def test_ls(capsys):
    config.ls()
    assert capsys.readouterr().out == "base.yaml\nplatform/ursa.yaml\nworkflow/rocoto.yaml\n"


@pytest.mark.parametrize("key_path", ["base.yaml", "platform/ursa.yaml"])
def test_show(capsys, key_path):
    config.show(key_path)
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
