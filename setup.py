"""
Basic setuptools configuration.

See https://setuptools.pypa.io/en/latest/userguide/quickstart.html#basic-use for information on
this standard setuptools file.

Here it is used 1. By conda-build to install the source files into the package tree; 2. By "make
devshell" to perform an "editable" install into the conda development environment, such that source
files in the clone are live-linked into the conda environment so that they can be executed in a
context where all build/run/test dependency packages are available; and 3. By pip users to install
the local package along with its dependencies from PyPI.
"""

import json
import os
import re
from pathlib import Path

from setuptools import find_packages, setup

# Collect package metadata.

recipe = Path(os.environ.get("RECIPE_DIR", "recipe"))
metasrc = recipe / "meta.json"
meta = json.loads(metasrc.read_text())
name_conda = meta["name"]
name_py = name_conda.replace("-", "_")
readme = Path(__file__).resolve().parent / "README.md"
src = "." if os.environ.get("CONDA_BUILD") else "src"

# Define basic setup configuration.

kwargs = {
    "description": "TBD",
    "entry_points": {"console_scripts": ["rheos = %s.cli:main" % name_py]},
    "include_package_data": True,
    "name": name_conda,
    "packages": find_packages(
        exclude=["%s.tests" % name_py], include=[name_py, "%s.*" % name_py], where=src
    ),
    "package_dir": {"": src},
    "version": meta["version"],
}

if readme.is_file():
    kwargs["long_description"] = readme.read_text()
    kwargs["long_description_content_type"] = "text/markdown"
elif os.environ.get("PYPI_PROJECT_NAME"):
    msg = "Required README not found: %s" % readme
    raise FileNotFoundError(msg)

# Define dependency packages for non-devshell installs, translating conda -> PyPI package names.

conda_pypi_name_map = {"uwtools": "unified-workflow-tools"}
do_not_install = ["python"]
pkgs = meta["packages"]["run"]

for k, v in conda_pypi_name_map.items():
    pkgs = [re.sub(rf"^{k}\b", v, pkg) for pkg in pkgs]

if not os.environ.get("CONDEV_SHELL"):
    kwargs["install_requires"] = [
        pkg.replace(" ==", "==")
        for pkg in pkgs
        if not any(re.match(rf"^{x} .*$", pkg) for x in do_not_install)
    ]

# Install.

setup(**kwargs)
