set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

detect() {
  if [[ -n "$(git status --porcelain)" ]]; then
    git --no-pager diff
    echo ERROR: Detected $1
    return 1
  fi
}

lint() {
  set -eux
  make format
  notrace detect "unformatted code: Run 'make format' to fix"
  make lint
}

notrace ci_conda_activate
make meta
notrace detect "out-of-date recipe/meta.json: Run 'make meta' to fix"
CONDEV_SHELL_CMD=lint notrace condev-shell
