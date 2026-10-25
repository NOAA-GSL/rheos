set -aeux

if [[ -v CONDA_BUILD || -v CONDEV_SHELL ]]; then
  echo "ERROR: Run make pypi-package outside condev-shell and conda-build." >&2
  exit 1
fi

# Prevent checkout paths from masking missing distribution files or dependencies.
unset PYTHONPATH RECIPE_DIR

# Use a temporary directory to isolate packaging test
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

# Build both distributions in an isolated environment, including the wheel from the sdist.
python -m venv "$workdir/build"
"$workdir/build/bin/python" -m pip install build twine
"$workdir/build/bin/python" -m build --outdir "$workdir/dist" "$root"
# Validate distribution metadata before attempting installation.
"$workdir/build/bin/python" -m twine check "$workdir"/dist/*

# Test the wheel in a clean environment, away from the checkout source tree.
python -m venv "$workdir/venv"
wheels=("$workdir"/dist/*.whl)
"$workdir/venv/bin/python" -m pip install "${wheels[0]}[dev]"
"$workdir/venv/bin/python" -m pip check

# Make sure tests pass for the installed wheel
mkdir "$workdir/test"
cp -R "$root/pyproject.toml" "$root/tests" "$workdir/test/"
cd "$workdir/test"
"$workdir/venv/bin/rheos" --version
"$workdir/venv/bin/pytest" --cov --cov-report=term-missing tests
