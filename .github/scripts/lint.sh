set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

detect() {
  set +x
  if [[ -n "$(git status --porcelain)" ]]; then
    git --no-pager diff
    echo DETECTED $1
    false
  fi
  set -x
}

lint() {
  set -eux
  make format
  detect "UNFORMATTED CODE"
  make lint
}

set +ux
ci_conda_activate
make meta
detect "OUT-OF-DATE META.JSON"
CONDEV_SHELL_CMD=lint condev-shell
