set -aeux

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

python -m pip install build twine
python -m build --outdir "$workdir/dist" "$root"
python -m twine check "$workdir"/dist/*

python -m venv "$workdir/venv"
wheels=("$workdir"/dist/*.whl)
"$workdir/venv/bin/python" -m pip install "${wheels[0]}[dev]"
"$workdir/venv/bin/python" -m pip check

mkdir "$workdir/test"
cp -R "$root/pyproject.toml" "$root/tests" "$workdir/test/"
cd "$workdir/test"
"$workdir/venv/bin/rheos" --version
"$workdir/venv/bin/pytest" --cov --cov-report=term-missing tests