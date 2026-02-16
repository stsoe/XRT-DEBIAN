#!/bin/bash
# Script to filter and build XRT-DEBIAN/src
# Run from within docker container

#set -e

# Get the directory where this script is located (TheRock root)
SCRIPT_DIR=$(readlink -f $(dirname ${BASH_SOURCE[0]}))
ROOT_DIR=$(readlink -f $SCRIPT_DIR/..)
HERE=$PWD

# Update submodules, can only done as user
# git submodule update --init --recursive

# Install build dependencies declared in the package's debian/control
cd $ROOT_DIR/src
apt-get build-dep -y xrt

# Copy and filter sources into /tmp
# Copy
mkdir -p /tmp/upstream/build
rsync -avz . /tmp/upstream/build/

# Filter
cd /tmp/upstream/build
/bin/rm -rf xdna/xdna-driver/xrt
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/ELFIO
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/lib/aie-rt
find . -type f -name .git -exec /bin/rm -rf {} \;
find . -type f -name .gitattributes -exec /bin/rm -rf {} \;
find . -type f -name .gitignore -exec /bin/rm -rf {} \;
find . -type f -name .gitmodules -exec /bin/rm -rf {} \;
find . -type d -name elf_examples -exec /bin/rm -rf {} \;
find . -type f -name usertest -exec /bin/rm -rf {} \;
find . -type f -name \*.elf -exec /bin/rm {} \;
find . -type f -name \*.a -exec /bin/rm {} \;
find . -type f -name \*.swn -exec /bin/rm {} \;
find . -type f -name \*.swo -exec /bin/rm {} \;
/bin/rm -rf xdna/xdna-driver/tools/bins

# Create the source archive from filtered sources
tar cvf /tmp/upstream/xrt-src.tar .

# Copy back to host, can only be done as user
# cp /tmp/upstream/xrt-src.tar <dst>

# Build
debuild -us -uc


