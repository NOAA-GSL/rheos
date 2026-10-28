from pathlib import Path

import pytest

from rheos.api import config
from rheos.util import resource_path


def test_catalog():
    assert config.catalog() == ["base.yaml", "platform/ursa.yaml", "workflow/rocoto.yaml"]


@pytest.fixture
def configs(mocker, tmp_path):
    # Mock the resource root, since test configs cannot be added to the installed package.
    mocker.patch.object(config, "_root", return_value=tmp_path)
    (tmp_path / "a.yaml").write_text("a: 1\nb: '{{ a }}'\n")
    (tmp_path / "x" / "y").mkdir(parents=True)
    (tmp_path / "x" / "y" / "b.yaml").write_text("c: 2\n")
    return ["a.yaml", "x/y/b.yaml"]


@pytest.mark.parametrize(
    ("realize", "b"),
    [(False, "{{ a }}"), (True, "1")],
)
def test_compose(b, capsys, configs, realize):
    result = config.compose(configs, realize=realize)
    assert result.data == {"a": 1, "b": b, "c": 2}
    assert "c: 2" in capsys.readouterr().out


def test_compose_to_dict(capsys, configs):
    result = config.compose_to_dict(configs)
    assert type(result) is dict
    assert result == {"a": 1, "b": "{{ a }}", "c": 2}
    assert not capsys.readouterr().out


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


@pytest.mark.parametrize("key_path", ["base.yaml", "platform/ursa.yaml"])
def test__node(key_path):
    assert config._node(key_path).read_text() == resource_path(Path("config", key_path)).read_text()


def test__root():
    assert {x.name for x in config._root().iterdir()} >= {"base.yaml", "platform", "workflow"}


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
