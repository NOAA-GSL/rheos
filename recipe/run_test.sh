#!/bin/bash

set -aeuo pipefail

# Tools:

cli() {
  msg Testing CLI
  rheos --version
  msg OK
}

format() {
  msg Formatting JSON
  for f in $(jsfiles); do
    jq -S . $f >$f.new || (echo "    in $f" && rm $f.new && false)
    if cmp --quiet $f.new $f; then
      rm $f.new
    else
      mv $f.new $f
    fi
  done
  msg Formatting shell code
  shfmt --indent 2 --write $(shfiles)
  msg Formatting Python code
  ruff format $(pyfiles)
  msg Sorting Python imports
  ruff check --select I --fix $(pyfiles)
  msg OK
}

lint() {
  msg Linting YAML
  yamllint --no-warnings $(yamlfiles)
  msg Linting shell code
  shellcheck --format=gcc --severity=info --shell=bash $(shfiles)
  msg Linting Python code
  ruff check $(pyfiles)
  msg OK
}

typecheck() {
  msg Typechecking Python code
  mypy $(pyfiles)
  msg OK
}

unittest() {
  msg Running Python unit tests
  pytest --cov=rheos --cov-report=term-missing --ignore=conda/ .
  msg OK
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
    file $x | grep -q "Bourne-Again shell script" && echo $x
  done | sort
}

yamlfiles() {
  find . -type f -name "*.yaml" -print | sort
}

# Main entrypoint:

if [[ ! -v CONDA_BUILD && ! -v CONDEV_SHELL ]]; then
  msg Not in development shell or conda-build process
  exit 1
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
  lint
  typecheck
  unittest
  cli
fi
