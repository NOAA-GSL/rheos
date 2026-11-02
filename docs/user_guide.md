# User Guide

[← Back to Index](index.md)

## Build Procedure

`rheos` requires users to provide executables for the components they intend to run. This procedure describes how to build those executables from the `rrfs-mpas-jedi` branch of the `rrfs-workflow` repository on Ursa.

### 1. Clone the repository

Clone the `rrfs-mpas-jedi` branch and initialize its submodules:

```text
git clone -b rrfs-mpas-jedi https://github.com/NOAA-EMC/rrfs-workflow
cd rrfs-workflow
git submodule update --init --recursive
```

Some nested submodules are configured with `update = none` and will be skipped during initialization.

### 2. Build the components

The following components have been successfully built on Ursa:

| Component    | Build command     | Executable(s)                                   |
|---|---|---|
| WPS (ungrib) | `./build.wps`     | `ungrib.x`                                      |
| MPAS         | `./build.mpas`    | `init_atmosphere_model.x`, `atmosphere_model.x` |
| MPASSIT      | `./build.mpassit` | `mpassit.x`                                     |
| UPP          | `./build.upp`     | `upp.x`                                         |

All build commands should be executed from the `rrfs-workflow/sorc` directory:

```text
cd sorc/
./build.wps
./build.mpas
./build.mpassit
./build.upp
```

Each build script automatically configures its required environment. No manual module loading is necessary before building.

The resulting executables are placed in `rrfs-workflow/exec`.

### 3. Configure the runtime environment

The following commands load the module environments for running the executables on Ursa. Execute them from the repository root.

MPAS and WPS:

```text
module purge
module use "$PWD/modulefiles"
module load rrfs/ursa.intel
```

MPASSIT:

```text
module purge
module use "$PWD/sorc/MPASSIT/modulefiles"
module load build.ursa.intel
```

UPP:

```text
module purge
module use "$PWD/sorc/UPP/modulefiles"
module load ursa_intel
```

[← Back to Index](index.md)
