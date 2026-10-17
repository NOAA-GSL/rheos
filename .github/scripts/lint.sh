set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

detect() {
  if [[ -n "$(git status --porcelain)" ]]; then
    git --no-pager diff
    echo "ERROR: Detected $*"
    return 1
  fi
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
