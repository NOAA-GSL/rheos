import json
from pathlib import Path

from pytest import mark

from rheos import util

# Tests


def test_pkgname():
    assert util.pkgname == "rheos"


@mark.parametrize("relpath", ["info.json", Path("info.json")])
def test_resource(relpath):
    assert json.loads(util.resource(relpath))["version"]


@mark.parametrize("relpath", ["info.json", Path("info.json")])
def test_resource_path(relpath):
    path = util.resource_path(relpath)
    assert path.name == "info.json"
    assert path.is_file()
