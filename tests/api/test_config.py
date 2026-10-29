from pytest import fixture, mark

from rheos.api import config

# Fixtures


@fixture
def configs(config_root):  # noqa: ARG001
    return ["a.yaml", "x/y/b.yaml"]


# Tests


@mark.parametrize(
    ("key_path", "expected"), [("a.yaml", "a: 1\nb: '{{ a }}'\n"), ("x/y/b.yaml", "c: 2\n")]
)
@mark.usefixtures("config_root")
def test_cat(capsys, expected, key_path):
    config.cat(key_path)
    assert capsys.readouterr().out == expected


@mark.usefixtures("config_root")
def test_catalog():
    assert config.catalog() == ["a.yaml", "x/y/b.yaml"]


@mark.parametrize(
    ("realize", "b"),
    [(False, "{{ a }}"), (True, "1")],
)
def test_compose(b, capsys, configs, realize):
    result = config.compose(configs, realize=realize)
    assert result.data == {"a": 1, "b": b, "c": 2}
    assert "c: 2" in capsys.readouterr().out


@mark.parametrize(
    ("realize", "b"),
    [(False, "{{ a }}"), (True, "1")],
)
def test_compose_to_dict(b, capsys, configs, realize):
    result = config.compose_to_dict(configs, realize=realize)
    assert type(result) is dict
    assert result == {"a": 1, "b": b, "c": 2}
    assert not capsys.readouterr().out


@mark.usefixtures("config_root")
def test_compose_to_dict_filesystem_and_resources(tmp_path):
    other = tmp_path / "other.yaml"
    other.write_text("a: 2\nd: 3\n")
    result = config.compose_to_dict(["a.yaml", str(other), "x/y/b.yaml"])
    assert result == {"a": 2, "b": "{{ a }}", "c": 2, "d": 3}


@mark.usefixtures("config_root")
def test_ls(capsys):
    config.ls()
    assert capsys.readouterr().out == "a.yaml\nx/y/b.yaml\n"


@mark.parametrize(
    ("key_path", "expected"),
    [(["a.yaml"], "a: 1\nb: '{{ a }}'\n"), (["x", "y", "b.yaml"], "c: 2\n")],
)
@mark.usefixtures("config_root")
def test_read(expected, key_path):
    assert config.read(key_path) == expected


@mark.parametrize(
    ("key_path", "expected"), [("a.yaml", "a: 1\nb: '{{ a }}'\n"), ("x/y/b.yaml", "c: 2\n")]
)
@mark.usefixtures("config_root")
def test__node(expected, key_path):
    assert config._node(key_path).read_text() == expected


@mark.usefixtures("config_root")
def test__paths(monkeypatch, tmp_path):
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    (cwd / "a.yaml").write_text("a: 2\n")  # shadows the a.yaml config resource
    other = tmp_path / "other.yaml"
    other.write_text("d: 3\n")
    with config._paths(["a.yaml", str(other), "x/y/b.yaml"]) as paths:
        assert [path.read_text() for path in paths] == ["a: 2\n", "d: 3\n", "c: 2\n"]


def test__root():
    root = config._root()
    assert root.name == "config"
    assert (root / "__init__.py").is_file()


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
