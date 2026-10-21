# rheos

## This repository is in active development.

## Developer Setup (conda)

1. If you do not already have a conda installation you want to reuse, install the [Miniforge](https://github.com/conda-forge/miniforge) conda appropriate for your system (Linux `aarch64` shown here), ideally not your git clone:

    ```
    wget https://github.com/conda-forge/miniforge/releases/download/26.7.2-0/Miniforge3-Linux-aarch64.sh
    bash Miniforge3-Linux-aarch64.sh -bfp /your/conda/path
    rm Miniforge3-Linux-aarch64.sh
    ```

1. Activate your conda's `base` environment:

    ```
    . /your/conda/path/etc/profile.d/conda.sh
    conda activate base
    ```

1. Install the [condev](https://anaconda.org/channels/maddenp/packages/condev/overview) package into your conda's `base` environment.

    ```
    conda install -y maddenp::condev
    ```

    If you cannot or do not want to install this package into your `base` environment, you can install it into a custom environment, e.g.:
    
    ```
    conda create -y -n condev maddenp::condev
    conda activate condev
    ```
    
    Hereafter, activate this custom environment instead of `base` for `rheos` work.

1. In the `rheos` git clone root, create and enter the development shell:

    ```
    make devshell
    ```

You will now be inside a shell with the `DEV-rheos` environment activate. Note that:

- The code under `src/rheos` is live-linked into the environment, such that any code changes take immediate local effect.
- All runtime and test packages are available, so `make` targets like `make format` and `make test` -- which will also be executed during package build and by CI -- function correctly.
- You can simply exit the shell to return to your previous shell.
- Future invocations of `make devshell` will be much faster since the development environment will already exist.
- If you make changes to files under `recipe/` and so need to rebuild the development environment, exit the shell, run `conda env remove -y -n DEV-rheos`, then run `make devshell` again. The `recipe/meta.json` file should be refreshed based on the current contents of `recipe/meta.yaml`, and you should commit these changes.
- If you need multiple development environments, you can precede `make devshell` with `DEV_ENV_PREFIX=<name>`, e.g. `DEV_ENV_PREFIX=FOO` will create (or activate if already created) development environment `FOO-rheos`.
- You can run `conda clean --all --yes` to reclaim disk space by purging unused cached packages.

## Developer Setup (pip)

1. Using Python 3.11 through 3.14, create a virtual environment outside the git clone:

    ```bash
    python -m venv ~/.venvs/rheos-dev
    ```

2. Activate the virtual environment:

    ```bash
    source ~/.venvs/rheos-dev/bin/activate
    ```

3. In the `rheos` git clone root, install the project and its development tools:

    ```bash
    python -m pip install -e '.[dev]'
    ```

### Important Notes

- The code under `src/rheos` is live-linked into the environment, so source changes take immediate effect.
- The `make cli`, `make format`, `make lint`, `make test`, `make typecheck`, and `make unittest` targets are fully supported.
- The `make devshell`, `make meta`, and `make package` targets remain conda-based workflows and are not supported by the pip-only setup.
- Keep the virtual environment outside the git clone so formatting and test tools do not scan its installed packages.
- Run `deactivate` to leave the virtual environment. Activate it again before returning to development.
