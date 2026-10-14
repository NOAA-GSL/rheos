# rheos

## This repository is in active development.

## Developer Setup

1. If you do not already have a conda installation you want to reuse (not that you must be able to install packages into its `base` environment), install the [Miniforge](https://github.com/conda-forge/miniforge) conda appropriate for your system (Linux `aarch64` shown here), ideally not your git clone:

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
