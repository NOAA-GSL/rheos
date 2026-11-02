# User Guide

[← Back to Index](index.md)

## Build Procedure

`rheos` requires users to provide executables for the components they intend to run. This procedure describes how to build those executables from the RRFS-MPAS-JEDI workflow repository on Ursa.

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

| Component | Build command | Executable(s) |
|---|---|---|
| WPS (ungrib) | `./build.wps`     | `ungrib.x` |
| MPAS         | `./build.mpas`    | `init_atmosphere_model.x`, `atmosphere_model.x` |
| MPASSIT      | `./build.mpassit` | `mpassit.x` |
| UPP          | `./build.upp`     | `upp.x` |

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

Other components supported by `build.all`, including `MPASBlend`, `rank_run`, `RDAS`, and `RRFS_UTILS`, were not tested as part of this procedure. The alternative MPAS CMake build has also not been tested.

### 3. Configure the runtime environment

To load the RRFS runtime environment on Ursa, execute the following commands from the repository root:

```text
module purge
module use "$PWD/modulefiles"
module load rrfs/ursa.intel
```

[← Back to Index](index.md)
