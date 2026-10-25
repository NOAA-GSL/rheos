export RECIPE_DIR := $(shell cd ./recipe && pwd)

CHANNELS := $(addprefix -c ,$(shell tr '\n' ' ' <$(RECIPE_DIR)/channels)) -c local
METADEPS := $(addprefix $(RECIPE_DIR)/,meta.yaml) src/rheos/resources/info.json
METAJSON := $(RECIPE_DIR)/meta.json
SHELL    := $(shell which bash)
TARGETS  := cli devshell docs format lint meta package pypi-package test typecheck unittest

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

cli:
	@recipe/run_test.sh cli

devshell:
	condev-shell || true

docs:
	@recipe/run_test.sh docs

format:
	@recipe/run_test.sh format

lint:
	@recipe/run_test.sh lint

meta: $(METAJSON)

package:
	conda build $(CHANNELS) --error-overlinking --override-channels $(RECIPE_DIR)

pypi-package:
	@.github/scripts/pypi-package.sh

test:
	@recipe/run_test.sh

typecheck:
	@recipe/run_test.sh typecheck

unittest:
	@recipe/run_test.sh unittest

$(METAJSON): $(METADEPS)
	condev-meta
