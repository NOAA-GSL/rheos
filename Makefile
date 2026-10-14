SHELL   := $(shell which bash)
TARGETS := format lint test typecheck unittest

.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

format:
	@./run format

lint:
	@./run lint

test: lint typecheck unittest

typecheck:
	@./run typecheck

unittest:
	@./run unittest
