set -aeux

. $(dirname ${BASH_SOURCE[0]})/common.sh

run_tests() {
  set -eux
  channels=$(xargs -d "\n" -I@ echo --channel @ <recipe/channels)
  devpkgs=$(jq .packages.dev[] recipe/meta.json | tr -d ' "')
  notrace conda create --yes --name rheos --quiet $channels $devpkgs python=$PYTHON_VERSION
  notrace conda activate rheos
  git clean -dfx
  pip install --editable src
  make cli
  make typecheck
  make unittest
}

if [[ ! -v PYTHON_VERSION ]]; then
  echo "PYTHON_VERSION must be set" >&2
  return 1
fi

set +ux
ci_conda_activate
CONDEV_SHELL_CMD=run_tests condev-shell
