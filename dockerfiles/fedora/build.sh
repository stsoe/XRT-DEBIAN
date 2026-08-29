#!/bin/bash
# This build script prepares the staging repo
# - https://github.com/stsoe/XRT-DEBIAN
# for rpmbuild through xrt.spec.
#
# The script creates a new tarball from the repo sources (this current
# clone) as opposed to using the tagged release tarball (see
# build-release.sh).  Otherwise the script behaves as
# build-release.sh and should be run within a Fedora docker container.
#
# Use this script to validate new repo sources and to create a tarball
# for a new tagged release.

set -euo pipefail

SCRIPT_DIR=$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")
# dockerfiles/fedora -> repository root
ROOT_DIR=$(readlink -f "${SCRIPT_DIR}/../..")

SPEC_SRC="${ROOT_DIR}/src/fedora/xrt.spec"
if [[ ! -f "${SPEC_SRC}" ]]; then
  echo "error: missing spec: ${SPEC_SRC}" >&2
  exit 1
fi

VERSION=$(awk '/^Version:/{print $2; exit}' "${SPEC_SRC}")
if [[ -z "${VERSION}" ]]; then
  echo "error: could not read Version from ${SPEC_SRC}" >&2
  exit 1
fi

RPMTOPDIR="${RPMTOPDIR:-${HOME}/rpmbuild}"

echo "==> Installing BuildRequires from spec (dnf builddep)"
dnf -y builddep "${SPEC_SRC}"

echo "==> Staging filtered sources under /tmp/upstream (same filters as Debian build.sh)"
/bin/rm -rf /tmp/upstream
mkdir -p /tmp/upstream/build
rsync -a "${ROOT_DIR}/src/" /tmp/upstream/build/

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

echo "==> Installing spec and tarball into ${RPMTOPDIR}"
install -D -m0644 "${SPEC_SRC}" "${RPMTOPDIR}/SPECS/xrt.spec"
install -D -m0644 "/tmp/upstream/xrt-${VERSION}.tar.gz" "${RPMTOPDIR}/SOURCES/xrt-${VERSION}.tar.gz"

echo "==> Installing patches to ${RPMTOPDIR}/SOURCES"
# Check and copy Debian patches
debian_patches=(${ROOT_DIR}/src/debian/patches/*.patch)
if [ -e "${debian_patches[0]}" ]; then
    cp "${debian_patches[@]}" "${RPMTOPDIR}/SOURCES"
fi

# Check and copy Fedora patches
fedora_patches=(${ROOT_DIR}/src/fedora/patches/*.patch)
if [ -e "${fedora_patches[0]}" ]; then
    cp "${fedora_patches[@]}" "${RPMTOPDIR}/SOURCES"
fi

echo "==> Installing manpages ${RPMTOPDIR}/SOURCES"
cp ${ROOT_DIR}/src/debian/man/* ${RPMTOPDIR}/SOURCES

echo "==> rpmbuild -ba"
export CCACHE_DIR="/scratch/ccache/rpmbuild"
mkdir -p $CCACHE_DIR
export CC="ccache gcc"
export CXX="ccache g++"
rpmbuild -ba --noclean "${RPMTOPDIR}/SPECS/xrt.spec"
ccache --show-stats || true
