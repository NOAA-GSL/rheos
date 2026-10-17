set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

test_suite() {
  set -eux
  notrace conda install --yes python=$PYTHON_VERSION
  pip install --editable src # corrects Python version in entry-point script
  make cli
  make typecheck
  make unittest
}

if [[ ! -v PYTHON_VERSION ]]; then
  echo "PYTHON_VERSION must be set" >&2
  false
fi

notrace ci_conda_activate
CONDEV_SHELL_CMD=test_suite notrace condev-shell
