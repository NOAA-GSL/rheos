set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

notrace ci_conda_activate
CONDEV_SHELL_CMD='make docs' notrace condev-shell
