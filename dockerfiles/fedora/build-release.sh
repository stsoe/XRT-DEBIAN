#!/bin/bash
# Filter sources and run rpmbuild for src/fedora/xrt.spec (Fedora analogue of
# dockerfiles/build.sh for Debian). Run inside the Fedora container with the
# repo mounted at /workspace/XRT-DEBIAN (see docker-run-fed.sh).
#
# Patches are applied in the spec %%prep step (debian/patches/series); do not
# run quilt here.

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
     "https://github.com/Xilinx/XRT/releases/download/${VERSION}/${VERSION}.tar.gz"

echo "==> Verifying checksum (optional but recommended)"
# Add SHA256SUMS check here if available from releases page

echo "==> Repackage tarbal with top-level directory"

/bin/rm -rf xrt-${VERSION}
mkdir xrt-${VERSION}
tar -xf xrt-${VERSION}.tar.gz -C xrt-${VERSION}
tar -czf xrt-${VERSION}.tar.gz xrt-${VERSION}

echo "==> Installing spec and upstream tarball into ${RPMTOPDIR}"
install -D -m0644 "${SPEC_SRC}" "${RPMTOPDIR}/SPECS/xrt.spec"
install -D -m0644 "xrt-${VERSION}.tar.gz" "${RPMTOPDIR}/SOURCES/xrt-${VERSION}.tar.gz"

echo "==> Installing patches to ${RPMTOPDIR}/SOURCES"
cp ${ROOT_DIR}/src/debian/patches/*.patch ${RPMTOPDIR}/SOURCES
cp ${ROOT_DIR}/src/fedora/patches/*.patch ${RPMTOPDIR}/SOURCES

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

# OUT="${OUT:-/tmp/upstream/rpm-artifacts}"
# mkdir -p "${OUT}"
# find "${RPMTOPDIR}/RPMS" -type f -name '*.rpm' -print0 | xargs -0 -r cp -t "${OUT}/"
# find "${RPMTOPDIR}/SRPMS" -type f -name '*.rpm' -print0 | xargs -0 -r cp -t "${OUT}/" || true

# echo ""
# echo "rpmbuild topdir: ${RPMTOPDIR}"
# echo "Copied RPMs and SRPM to: ${OUT}"
# ls -la "${OUT}"
