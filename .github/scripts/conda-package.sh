set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

notrace ci_conda_activate
notrace conda install --yes conda-build
conda config --set anaconda_upload false
make package