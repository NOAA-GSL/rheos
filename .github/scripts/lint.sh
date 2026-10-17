set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

detect() {
  set +x
  if [[ -n "$(git status --porcelain)" ]]; then
    git --no-pager diff
    echo ERROR: Detected $1
    return 1
  fi
  set -x
}

lint() {
  set -eux
  make format
  detect "unformatted code: Run 'make format' to fix"
  make lint
}

set +ux
ci_conda_activate
make meta
detect "out-of-date recipe/meta.json: Run 'make meta' to fix"
CONDEV_SHELL_CMD=lint condev-shell
