from unittest.mock import patch

from pytest import fixture

from rheos.api import config

# Fixtures


@fixture
def config_root(tmp_path):
    """
    Provide a temporary config-resources tree in place of the real one.
    """
    files = {
        "__init__.py": "",
        "a.yaml": "a: 1\nb: '{{ a }}'\n",
        "x/__init__.py": "",
        "x/y/b.yaml": "c: 2\n",
    }
    for relpath, text in files.items():
        path = tmp_path / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    # Mock the resource root, since test configs cannot be added to the installed package, and the
    # real resources will change over time.
    with patch.object(config, "_root", return_value=tmp_path):
        yield tmp_path
