set -aeux

if [[ -v CONDA_BUILD || -v CONDEV_SHELL ]]; then
  echo "ERROR: Run make pip-package outside condev-shell and conda-build." >&2
  exit 1
fi

# Prevent checkout paths from masking missing distribution files or dependencies.
unset PYTHONPATH RECIPE_DIR

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

python -m venv "$workdir/build"
"$workdir/build/bin/python" -m pip install build twine
"$workdir/build/bin/python" -m build --outdir "$workdir/dist" "$root"
"$workdir/build/bin/python" -m twine check "$workdir"/dist/*

python -m venv "$workdir/venv"
wheels=("$workdir"/dist/*.whl)
"$workdir/venv/bin/python" -m pip install "${wheels[0]}[dev]"
"$workdir/venv/bin/python" -m pip check

mkdir "$workdir/test"
cp -R "$root/pyproject.toml" "$root/tests" "$workdir/test/"
cd "$workdir/test"
"$workdir/venv/bin/rheos" --version
"$workdir/venv/bin/pytest" --cov --cov-report=term-missing tests