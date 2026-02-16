# XRT-DEBIAN
Mono repository for building AMD XDNA user space components for upstream
to Debian.

## Code base
The repository is a lightweight mono repo made up from following submodules

- xdna-driver: https://github.com/amd/xdna-driver
- XRT: https://github.com/Xilinx/XRT

### Content
Besides the submodule pointers, this repo contains Dockerfiles
and build scripts for building the upstream packages using `debuild`.

```
.
├── dockerfiles
│   ├── build.sh                    # build script executed within docker container
│   ├── debian_unstable.Dockerfile  # Dockerfile 
│   ├── docker-build.sh             # Build docker container manually
│   └── docker-run.sh               # Run the manually built docker container
├── LICENSE                         # Apache-2.0
├── README.md                       # This file
└── src
    ├── CMakeLists.txt              # Top-level CMakefile invoked by debian/rules
    ├── debian/                     # Meta-data for Debian build
    ├── xdna
    │   ├── CMakeLists.txt
    │   └── xdna-driver/            # xdna-driver submodule
    └── xrt
        ├── CMakeLists.txt
        └── XRT/                    # XRT submodule
```

The git hash of the `XRT` submodule pointer is exactly the 
git hash of `xdna-driver/xrt`.  This is not enforced, but any official 
source package for Debian upstreaming must ensure matching submodules.

## Github workflow
Any PR to this repo triggers a pr-build (`.github/workflows/pr-build.yml`).

The PR build, recursively clones the repo, creates a docker container
in which `debuild` is run.  The artifacts from the build are saved as
artifacts upload.

## Create a release build
Release builds are created from tagged submodules, e.g. 

- xdna-driver: https://github.com/amd/xdna-driver/releases/tag/2.21.75
- XRT: https://github.com/Xilinx/XRT/releases/tag/2.21.75

XRT (`xrt-smi`) has an implicit dependency on test validatation data
from the `VTD` repository.  Alas, VTD must be tagged accordingly to
ensure that the dependency matches the expectations for the userspace
code. For example (matching the above xdna-driver and XRT tags):

- VTD: https://github.com/Xilinx/VTD/releases/tag/2.21.75

> [!IMPORTANT]
> The top-level `CMakeLists.txt` file must be updated to specify the
> build number (e.g. `75`), which is baked into the binaries created
> from the build.  The build number ensures that `xrt-smi` attempts to 
> locate validation data that is compatible with the build.

If the validation data is missing at run-time, `xrt-smi` will report
failure and user must manually install artifacts into a
`XDG_DATA_HOME` directory. For example, for Strix, one would have to
use `wget` or `curl` to install
https://github.com/Xilinx/VTD/blob/2.21.75/archive/strx/xrt_smi_strx.a
into `$HOME/.local/share/xrt/2.21.75/amdxdna/bins/`

## Manually building a current cloned repo

To pre-validate clone repo sources, use this recipe:

1. Ensure all submodules are updated recursively
2. `cd dockerfiles/`
3. Use `./docker-build.sh` to create a Docker images for debian-unstable
4. Use `./docker-run.sh` to start and instance of the docker image
3. Run `./build.sh` within the docker instance.

The `build.sh` will run the build in `/tmp/upstream` and leave all
artifacts under that directory.

Once satisfied with the build, raise a PR, which will kick off the 
GitHub workflow and upload artifacts.

## Creating an XRT release with upstream source package
Once a release is merged to the XRT-DEBIAN repo, the workflow
can be kicked off manually to create the artifacts and source
package that must be provided to Debian maintainer.

Current conventions is to attach the source package to the XRT tagged
release as was done here: https://github.com/Xilinx/XRT/releases/tag/2.21.75

To upload source package, use `gh` (install `gh` if necessary)
```
% cd <path>/XRT clone
# To add artifacts 
% gh release upload 2.21.75 /home/stsoe/git/stsoe/upstream/XRT-DEBIAN/artifacts/2.21.75.tar.gz

# To remove artifacts (in case of error)
% gh release delete-asset 2.21.75 2.21.75.tar.gz
```
