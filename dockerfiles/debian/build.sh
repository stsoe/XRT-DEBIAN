#!/bin/bash
# Script to filter and build XRT-DEBIAN/src
# Run from within docker container

#set -e

# Get the directory where this script is located (TheRock root)
SCRIPT_DIR=$(readlink -f $(dirname ${BASH_SOURCE[0]}))
ROOT_DIR=$(readlink -f $SCRIPT_DIR/../..)
HERE=$PWD

# Update submodules, can only done as user
# git submodule update --init --recursive

# Install build dependencies declared in the package's debian/control
cd $ROOT_DIR/src

# Cleanup from previous builds
/bin/rm -rf /tmp/upstream

# Copy and filter sources into /tmp
# Copy
mkdir -p /tmp/upstream/build
rsync -avz . /tmp/upstream/build/

# Filter
cd /tmp/upstream/build
/bin/rm -rf fedora
/bin/rm -rf xdna/xdna-driver/xrt
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/ELFIO
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/lib/aie-rt
/bin/rm -rf xrt/XRT/src/runtime_src/core/edge/user/test
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/publish
/bin/rm -rf xrt/XRT/src/runtime_src/aie-rt/driver/tests/utest/elf_files
find . -type f -name .git -exec /bin/rm -rf {} \;
find . -type f -name .gitattributes -exec /bin/rm -rf {} \;
find . -type f -name .gitignore -exec /bin/rm -rf {} \;
find . -type f -name .gitmodules -exec /bin/rm -rf {} \;
find . -depth -type d -name elf_examples -exec /bin/rm -rf {} +
find . -type f -name usertest -exec /bin/rm -rf {} \;
find . -type f -name \*.elf -exec /bin/rm {} \;
find . -type f -name \*.a -exec /bin/rm {} \;
find . -type f -name \*.swn -exec /bin/rm {} \;
find . -type f -name \*.swo -exec /bin/rm {} \;
/bin/rm -rf xdna/xdna-driver/tools/bins

# Create the source archive from filtered sources. We don't apply
# patches here because they are applied on the extracted tarball
# sources by the build.
tar cvfJ /tmp/upstream/xrt-src.tar.xz .

# Apply patches. For local native builds (see debian/source/format)
# debuild does not apply patches automatically.
QUILT_PATCHES=debian/patches quilt push -a

# Copy back to host, can only be done as user
# cp /tmp/upstream/xrt-src.tar <dst>

# Install build dependencies declared in the package's debian/control
apt-get update
mk-build-deps --install --tool='apt-get -y' debian/control

# Doesn't seem to come in build-dep, so install manually
apt-get install libamdhip64-dev appstream -y

# ccache with debuild doesn't appear to work
#export CCACHE_DIR="/scratch/ccache/debuild"
#mkdir -p $CCACHE_DIR
#export CC="ccache cc"
#export CXX="ccache c++"

# Build
debuild -us -uc

#ccache --show-stats || true

