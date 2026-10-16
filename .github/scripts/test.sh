. $(dirname ${BASH_SOURCE[0]})/common.sh

run_tests() {
  if [[ -z ${PYTHON_VERSION:-} ]]; then
    echo "PYTHON_VERSION must be set" >&2
    return 1
  fi
  echo TESTING PYTHON $PYTHON_VERSION
  env=python-$PYTHON_VERSION
  devpkgs=$(jq .packages.dev[] recipe/meta.json | tr -d ' "')
  conda create --yes --name $env --quiet $devpkgs
  conda activate $env
  conda install --yes python=$PYTHON_VERSION
  set -x
  git clean -dfx
  pip install --editable src # sets new Python version in entry-point scripts
  make test
  status=$?
  set +x
  conda deactivate
  return $status
}

ci_conda_activate
CONDEV_SHELL_CMD=run_tests condev-shell
