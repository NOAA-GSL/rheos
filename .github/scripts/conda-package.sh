set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

notrace ci_conda_activate
conda config --set anaconda_upload false
make package