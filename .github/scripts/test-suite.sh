set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

run_tests() {
  set -eux
  devpkgs=$(jq .packages.dev[] recipe/meta.json | tr -d ' "')
  set +ux
  conda create --yes --name rheos --quiet $devpkgs
  conda activate rheos
  conda install --yes python=$PYTHON_VERSION
  set -ux
  git clean -dfx
  pip install --editable src
  make cli
  make typecheck
  make unittest
  set +x
}

if [[ ! -v PYTHON_VERSION ]]; then
  echo "PYTHON_VERSION must be set" >&2
  return 1
fi

set +ux
ci_conda_activate
CONDEV_SHELL_CMD=run_tests condev-shell
