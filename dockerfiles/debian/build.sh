#!/bin/bash
# Script to filter and build XRT-DEBIAN/src
# Run from within docker container

#set -e

# Get the directory where this script is located (TheRock root)
SCRIPT_DIR=$(readlink -f $(dirname ${BASH_SOURCE[0]}))
ROOT_DIR=$(readlink -f $SCRIPT_DIR/../..)
HERE=$PWD
VERSION=2.25.0

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
${ROOT_DIR}/dockerfiles/common/filter-sources.sh

# Create the source archive from filtered sources. We don't apply
# patches here because they are applied on the extracted tarball
# sources by the build.
/bin/rm -f "xrt-${VERSION}.tar.gz"
tar \
  --exclude='debian' \
  --exclude='fedora' \
  --transform "s,^\(\./\)\?,xrt-${VERSION}/," \
  --exclude-vcs \
  -czf "xrt-${VERSION}.tar.gz" .

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

