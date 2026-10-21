# Contributor Guide

[← Back to Index](index.md)

Welcome to the `rheos` Contributor Guide. Please familiarize yourself with and follow the procedures in the sections below before submitting changes.

> **Note:** Before starting work on a new feature, bug fix, or other change, please open an [Issue](https://github.com/NOAA-GSL/rheos/issues) to propose your change and solicit feedback from other developers. This helps avoid duplicate efforts or wasted work.

## Table of Contents

- [Developer Setup (conda)](#developer-setup-conda)
- [Developer Setup (pip)](#developer-setup-pip)
- [Code Quality](#code-quality)
- [API Documentation](#api-documentation)
- [Fork and PR Model](#fork-and-pr-model)
  - [Overview](#overview)
  - [Specifics for rheos](#specifics-for-rheos)
  - [Merging](#merging)
  - [Need Help?](#need-help)

## Developer Setup (conda)

Rheos development uses a conda environment managed by [condev](https://anaconda.org/channels/maddenp/packages/condev/overview). If an existing, writable conda installation is not available, install a [Miniforge](https://github.com/conda-forge/miniforge) distribution appropriate for the development system. Install Miniforge outside the Rheos clone when possible.

Activate the `base` environment of the conda installation, then install `condev`:

```text
conda install -y maddenp::condev
```

`condev` may instead be installed in a dedicated environment. Activate that environment rather than `base` before working on Rheos:

```text
conda create -y -n condev maddenp::condev
conda activate condev
```

From the root of a Rheos clone, create and enter the development shell:

```text
make devshell
```

The development shell activates the `DEV-rheos` environment. The code under `src/rheos` is installed in editable mode, so source changes take effect immediately. It also provides Rheos's runtime dependencies and code-quality tools. Exit the shell to return to the previously active shell.

Subsequent `make devshell` invocations reuse the existing environment. If changes to `recipe/` require rebuilding it, exit the development shell, remove the environment, and create it again:

```text
conda env remove -y -n DEV-rheos
make devshell
```

`make devshell` refreshes `recipe/meta.json` when its dependencies change. If `recipe/meta.yaml` is changed outside a development shell, run `make meta` from an activated conda environment with `condev` installed, then include the resulting `recipe/meta.json` update in the change.

To use a different development-environment name, set `DEV_ENV_PREFIX` when invoking the target:

```text
DEV_ENV_PREFIX=feature make devshell
```

## Developer Setup (pip)

1. Using Python 3.11 through 3.14, create a virtual environment outside the git clone:

    ```text
    python -m venv ~/.venvs/rheos-dev
    ```

2. Activate the virtual environment:

    ```text
    source ~/.venvs/rheos-dev/bin/activate
    ```

3. In the `rheos` git clone root, install the project and its development tools:

    ```text
    python -m pip install -e '.[dev]'
    ```

### Important Notes

- The code under `src/rheos` is live-linked into the environment, so source changes take immediate effect.
- The `make cli`, `make docs`, `make format`, `make lint`, `make test`, `make typecheck`, and `make unittest` targets are fully supported.
- The `make devshell`, `make meta`, and `make package` targets remain conda-based workflows and are not supported by the pip-only setup.
- Keep the virtual environment outside the git clone so formatting and test tools do not scan its installed packages.
- Run `deactivate` to leave the virtual environment. Activate it again before returning to development.

## Code Quality

Run the following targets from an active conda development shell or pip virtual environment:

| Target | Description |
| --- | --- |
| `make format` | Formats Python with [ruff](https://docs.astral.sh/ruff/), JSON with Python, and Bash with [go-shfmt](https://github.com/mvdan/sh). |
| `make lint` | Lints Python with [ruff](https://docs.astral.sh/ruff/), Bash with [shellcheck](https://www.shellcheck.net/), and YAML with [yamllint](https://yamllint.readthedocs.io/). |
| `make typecheck` | Typechecks Python with [mypy](https://mypy.readthedocs.io/). |
| `make unittest` | Runs unit tests and reports coverage with [pytest](https://docs.pytest.org/) and [coverage](https://coverage.readthedocs.io/). |
| `make cli` | Checks the installed `rheos` command-line interface. |
| `make docs` | Builds HTML API documentation with [pdoc](https://pdoc.dev/) into `docs/api/`. |
| `make test` | Runs the CLI check, linting, type checking, and unit tests. |

Configuration for these tools is in `pyproject.toml`, `.shellcheckrc`, and `.yamllint.yaml` at the repository root. Rheos requires 100% branch coverage; `make unittest` enforces the configured coverage threshold.

Use the following command regularly while developing and before opening or updating a pull request:

```text
make format && make test
```

Formatting runs first because it can identify syntax problems that prevent later checks from running and can change reported line numbers. Linting provides a quick check for errors and anti-patterns, type checking validates Python interfaces, and unit tests check behavior after the earlier checks pass. CI checks formatting and linting, builds and tests the Conda package, validates the editable pip development install, and runs the test suite on Python 3.11 through 3.14 for pull requests and pushes.

## API Documentation

Rheos API reference material is generated from Python source docstrings. Public modules, classes, functions, and methods should therefore have accurate, useful docstrings that describe their purpose, parameters, return values, side effects, and exceptions where applicable. Keep docstrings and type annotations synchronized with implementation changes.

API documentation for the `rheos` Python module is generated from source-code docstrings with [pdoc](https://pdoc.dev/). Build it locally from an active conda development shell or pip virtual environment:

```text
make docs
```

Output is written to `docs/api/`, which is excluded from version control. Open `docs/api/index.html` in a browser to preview the API documentation. CI builds the API documentation for pull requests and pushes to all branches. Pushes to `main` publish it through GitHub Pages when Pages is enabled for the repository.

## Fork and PR Model

### Overview

Contributions to Rheos use the GitHub [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) and [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) model:

1. [Fork](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project#forking-a-repository) the [Rheos repository](https://github.com/NOAA-GSL/rheos) into a personal GitHub account.
1. [Clone](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project) the fork onto the development system.
1. Create an issue to discuss the proposed change before starting work.
1. [Create a branch](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project#creating-a-branch-to-work-on) for the change.
1. Make, commit, and push changes to the branch. Follow the [Developer Setup (conda)](#developer-setup-conda) or [Developer Setup (pip)](#developer-setup-pip) and [Code Quality](#code-quality) guidance.
1. [Create a pull request](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project#making-a-pull-request) to merge the branch into the main repository.

For future contributions, either recreate the fork or configure the official repository as an [upstream remote](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-repository-for-a-fork) and [sync the fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork).

### Specifics for rheos

When creating a pull request:

- Target base repository `NOAA-GSL/rheos` and base branch `main`.
- Complete the pull-request template with an informative synopsis, change type, impact, and the applicable checklist items.
- Open the pull request as a [draft](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests#draft-pull-requests) while the change is in progress.
- In the _Files changed_ tab, add inline comments where they will help reviewers understand non-obvious choices.
- Mark the pull request ready for review after it is complete, documented, formatted, and tested.

Code owners are automatically requested for review. Address review comments by committing and pushing updates to the pull-request branch; GitHub updates the pull request automatically.

### Merging

A pull request is ready to merge when required reviews and required CI checks have passed, and any outstanding review conversations have been resolved. These statuses appear at the bottom of the pull request's _Conversation_ tab. Contributors with write access may merge an eligible pull request; otherwise, a Rheos core developer will merge it.

### Need Help?

Ask questions about a proposed change or pull request in its _Conversation_ tab. Use the linked issue to discuss the broader scope or design of a change.
