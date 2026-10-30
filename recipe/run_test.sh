#!/usr/bin/env bash

set -aeuo pipefail

# Tools:

cli() {
  if [[ ! -v CONDA_BUILD ]]; then
    msg Testing CLI
    rheos --version
  fi
}

docs() {
  local outdir
  outdir=$PWD/docs/api
  msg Building documentation in $outdir
  PYTHONWARNINGS="ignore:Error parsing type annotation" pdoc --output-directory $outdir rheos.api
  msg Built documentation in $outdir
}

format() {
  local files
  files=($(jsfiles))
  if [[ ${#files[@]} -gt 0 ]]; then
    msg Formatting JSON
    for f in ${files[@]}; do
      python -m json.tool --sort-keys --indent 2 --no-ensure-ascii "$f" >"$f.new" ||
        (echo "    in $f" && rm "$f.new" && false)
      if cmp --quiet $f.new $f; then
        rm $f.new
      else
        mv $f.new $f
      fi
    done
  fi
  files=($(pyfiles))
  if [[ ${#files[@]} -gt 0 ]]; then
    msg Formatting Python code
    ruff format ${files[@]}
    msg Sorting Python imports
    ruff check --select I --fix ${files[@]}
  fi
  files=($(shfiles))
  if [[ ${#files[@]} -gt 0 ]]; then
    msg Formatting shell code
    shfmt --indent 2 --write ${files[@]}
  fi
}

lint() {
  local files
  files=($(pyfiles))
  if [[ ${#files[@]} -gt 0 ]]; then
    msg Linting Python code
    ruff check ${files[@]}
  fi
  files=($(shfiles))
  if [[ ${#files[@]} -gt 0 ]]; then
    msg Linting shell code
    shellcheck --format=gcc --severity=info --shell=bash ${files[@]}
  fi
  files=($(yamlfiles))
  if [[ ${#files[@]} -gt 0 ]]; then
    msg Linting YAML
    yamllint --no-warnings ${files[@]}
  fi
}

typecheck() {
  msg Typechecking Python code
  mypy $(pyfiles)
}

unittest() {
  msg Running Python unit tests
  pytest --cov --cov-report=term-missing .
}

# Helpers:

jsfiles() {
  find . -type f -name "*.json*" -print | sort
}

msg() {
  echo "=> $*"
}

pyfiles() {
  find . -type f -name "*.py" -print | sort
}

shfiles() {
  local x
  find . -type f -print | sort | while read -r x; do
    if file $x | grep -q "Bourne-Again shell script"; then
      echo $x
    fi
  done | sort
}

yamlfiles() {
  find . -type f -name "*.yaml" -print | sort
}

# Main entrypoint:

if [[ ! -v CONDA_BUILD && ! -v CONDEV_SHELL ]]; then
  for tool in mypy pytest ruff shellcheck shfmt yamllint; do
    if ! command -v "$tool" >/dev/null 2>&1; then
      msg "Missing development tool: $tool"
      msg "Activate the conda development shell or your Python virtual environment."
      msg "For pip-based development, run: python -m pip install -e '.[dev]'"
      exit 1
    fi
  done
fi

if [[ -v CONDA_BUILD ]]; then
  cd ../test_files
else
  cd $(dirname $0)/..
fi

if [[ -n "${1:-}" ]]; then
  # Run single tool:
  $1
else
  # Run all tools:
  cli
  lint
  typecheck
  unittest
fi
