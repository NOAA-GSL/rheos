set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

detect() {
  test -z "$(git status --porcelain)" && return 0
  git --no-pager diff
  echo "ERROR: Detected $*"
  return 1
}

lint() {
  set -eux
  make format
  notrace detect "unformatted code"
  make lint
}

notrace ci_conda_activate
make meta
notrace detect "out-of-date recipe/meta.json"
CONDEV_SHELL_CMD=lint notrace condev-shell
