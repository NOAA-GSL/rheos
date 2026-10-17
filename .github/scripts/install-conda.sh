set -eux

. $(dirname ${BASH_SOURCE[0]})/common.sh

url=https://github.com/conda-forge/miniforge/releases/download/26.7.2-0/Miniforge3-Linux-x86_64.sh
installer=/tmp/$(basename $url)
wget --no-verbose -O $installer $url
bash $installer -bfp $CI_CONDA_DIR
notrace ci_conda_activate
notrace conda install --yes --repodata-fn repodata.json jq maddenp::condev # anaconda-client python-build
