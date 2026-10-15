import json
from pathlib import Path

import pytest

from rheos import util


def test_pkgname():
    assert util.pkgname == "rheos"


@pytest.mark.parametrize("relpath", ["info.json", Path("info.json")])
def test_resource(relpath):
    assert json.loads(util.resource(relpath))["version"]


@pytest.mark.parametrize("relpath", ["info.json", Path("info.json")])
def test_resource_path(relpath):
    path = util.resource_path(relpath)
    assert path.name == "info.json"
    assert path.is_file()


def test_version(mocker):
    mocker.patch.object(util, "resource", return_value='{"version": "1.2.3", "buildnum": "4"}')
    assert util.version() == "version 1.2.3"
