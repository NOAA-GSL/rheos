set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

run_tests() {
  set -eux
  notrace conda install --yes python=$PYTHON_VERSION
  make cli
  make typecheck
  make unittest
}

if [[ ! -v PYTHON_VERSION ]]; then
  echo "PYTHON_VERSION must be set" >&2
  false
fi

set +ux
ci_conda_activate
CONDEV_SHELL_CMD=run_tests condev-shell
