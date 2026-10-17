set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

lint() {
  set -eux
  make format
  if [[ -n "$(git status --porcelain)" ]]; then
    git --no-pager diff
    (set +x && echo UNFORMATTED CODE DETECTED)
    false
  fi
  make lint
}

set +ux
ci_conda_activate
CONDEV_SHELL_CMD=lint condev-shell
