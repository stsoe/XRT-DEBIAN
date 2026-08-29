#!/bin/bash
# This build script prepares a tagged XRT release tarball for rpmbuild
# through xrt.spec. It should be run within a Fedora docker container
# (see docker-build.sh and docker-run.sh)

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

echo "==> Downloading official XRT tarball from GitHub"
cd /tmp
/bin/rm -f "xrt-${VERSION}.tar.gz"  # Use .gz to match upstream

# Download the official release tarball
curl -L -o "xrt-${VERSION}.tar.gz" \
     "https://github.com/Xilinx/XRT/releases/download/${VERSION}/xrt-${VERSION}.tar.gz"

echo "==> Installing spec and upstream tarball into ${RPMTOPDIR}"
install -D -m0644 "${SPEC_SRC}" "${RPMTOPDIR}/SPECS/xrt.spec"
install -D -m0644 "xrt-${VERSION}.tar.gz" "${RPMTOPDIR}/SOURCES/xrt-${VERSION}.tar.gz"

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
#rpmbuild -ba "${RPMTOPDIR}/SPECS/xrt.spec"
# build without clean (prevese buildroot for inspection)
rpmbuild -ba --noclean "${RPMTOPDIR}/SPECS/xrt.spec"
ccache --show-stats || true
