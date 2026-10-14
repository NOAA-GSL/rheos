export RECIPE_DIR := $(shell cd ./recipe && pwd)

CHANNELS := $(addprefix -c ,$(shell tr '\n' ' ' <$(RECIPE_DIR)/channels)) -c local
METADEPS := $(addprefix $(RECIPE_DIR)/,meta.yaml) src/rheos/resources/info.json
METAJSON := $(RECIPE_DIR)/meta.json
SHELL    := $(shell which bash)
TARGETS  := devshell format lint meta test typecheck unittest

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

devshell:
	condev-shell || true

format:
	@recipe/run_test.sh format

lint:
	@recipe/run_test.sh lint

meta: $(METAJSON)

test: lint typecheck unittest

typecheck:
	@recipe/run_test.sh typecheck

unittest:
	@recipe/run_test.sh unittest

$(METAJSON): $(METADEPS)
	condev-meta
