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

echo "==> Staging filtered sources under /tmp/upstream (same filters as Debian build.sh)"
/bin/rm -rf /tmp/upstream
mkdir -p /tmp/upstream/build
rsync -a "${ROOT_DIR}/src/" /tmp/upstream/build/

cd /tmp/upstream/build

/bin/rm -rf xdna/xdna-driver/xrt
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/ELFIO
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/lib/aie-rt
/bin/rm -rf xrt/XRT/src/runtime_src/core/edge/user/test
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/publish
/bin/rm -rf xrt/XRT/src/runtime_src/aie-rt/driver/tests/utest/elf_files
find . -type f -name .git -exec /bin/rm -rf {} \;
find . -type f -name .gitattributes -exec /bin/rm -f {} \;
find . -type f -name .gitignore -exec /bin/rm -f {} \;
find . -type f -name .gitmodules -exec /bin/rm -f {} \;
# Depth-first: avoid "No such file or directory" when rm -rf removes a dir
# find is still descending into (POSIX: deleting dirs during find is undefined).
find . -depth -type d -name elf_examples -exec /bin/rm -rf {} +
find . -type f -name usertest -exec /bin/rm -f {} \;
find . -type f -name '*.elf' -exec /bin/rm -f {} \;
find . -type f -name '*.a' -exec /bin/rm -f {} \;
find . -type f -name '*.swn' -exec /bin/rm -f {} \;
find . -type f -name '*.swo' -exec /bin/rm -f {} \;
/bin/rm -rf xdna/xdna-driver/tools/bins

echo "==> Creating Source0 tarball xrt-${VERSION}.tar.xz (GNU tar --transform)"
cd /tmp/upstream
/bin/rm -f "xrt-${VERSION}.tar.xz"
tar -C build \
  --transform "s,^,xrt-${VERSION}/," \
  --exclude-vcs \
  -caf "xrt-${VERSION}.tar.xz" .

echo "==> Installing spec and tarball into ${RPMTOPDIR}"
install -D -m0644 "${SPEC_SRC}" "${RPMTOPDIR}/SPECS/xrt.spec"
install -D -m0644 "/tmp/upstream/xrt-${VERSION}.tar.xz" "${RPMTOPDIR}/SOURCES/xrt-${VERSION}.tar.xz"

echo "==> rpmbuild -ba"
export CCACHE_DIR="/scratch/ccache/rpmbuild"
mkdir -p $CCACHE_DIR
export CC="ccache gcc"
export CXX="ccache g++"
rpmbuild -ba "${RPMTOPDIR}/SPECS/xrt.spec"
ccache --show-stats || true

OUT="${OUT:-/tmp/upstream/rpm-artifacts}"
mkdir -p "${OUT}"
find "${RPMTOPDIR}/RPMS" -type f -name '*.rpm' -print0 | xargs -0 -r cp -t "${OUT}/"
find "${RPMTOPDIR}/SRPMS" -type f -name '*.rpm' -print0 | xargs -0 -r cp -t "${OUT}/" || true

echo ""
echo "rpmbuild topdir: ${RPMTOPDIR}"
echo "Copied RPMs and SRPM to: ${OUT}"
ls -la "${OUT}"
