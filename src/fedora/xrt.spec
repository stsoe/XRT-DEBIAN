# SPDX-License-Identifier: Apache-2.0
# Spec layout mirrors src/debian/control and src/debian/rules.
#
# Source tarball: must unpack to one top-level directory xrt-%{version}/ (see %%setup -n).
# Example (GNU tar), run from the repository root:
#   tar -C src --transform 's,^,xrt-%{version}/,' --exclude-vcs -caf ~/rpmbuild/SOURCES/xrt-%{version}.tar.xz .
#
# Patches: applied in %prep from debian/patches/series (same order as quilt).
#
# HIP: requires ROCm-style dev packages on the build host (see BuildRequires).

%global debug_package %{nil}

Name:           xrt
Epoch:          0
Version:        2.21.75
Release:        1%{?dist}
Summary:        Xilinx / AMD FPGA and ACAP runtime (XRT), Debian-aligned subpackages

License:        Apache-2.0 AND GPL-2.0-only AND GPL-2.0-or-later
URL:            https://github.com/Xilinx/XRT

Source0:       %{name}-%{version}.tar.xz

# Architectures aligned with debian/control (lib* and python are arm64+amd64
ExclusiveArch:  aarch64 x86_64

BuildRequires:  cmake >= 3.16
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(yaml-cpp)
# Fedora rapidjson-devel provides pkgconfig(RapidJSON), not pkgconfig(rapidjson).
BuildRequires:  pkgconfig(RapidJSON)
BuildRequires:  pkgconfig(ocl-icd)
BuildRequires:  opencl-headers
BuildRequires:  boost-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-compiler
BuildRequires:  ncurses-devel
BuildRequires:  libuuid-devel
BuildRequires:  python3-devel
BuildRequires:  pybind11-devel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  doxygen
BuildRequires:  appstream
BuildRequires:  python3-rpm-macros
# HIP stack (Debian: libamdhip64-dev). On Fedora use distro ROCm packages when available.
BuildRequires:  rocm-hip-devel

%description
This source package builds the same binary package set as the Debian
packaging under src/debian: runtime libraries split for core / NPU / Alveo,
Python bindings, development files, and utilities.

%package -n libxrt2
Summary:        Xilinx Runtime (XRT) - runtime libraries

%description -n libxrt2
Xilinx Runtime library (XRT) is an open-source software stack for FPGA /
ACAP devices. This package provides the core runtime shared libraries
(equivalent to Debian libxrt2).

%package -n libxrt-npu2
Summary:        Xilinx Runtime (XRT) NPU - runtime libraries

%description -n libxrt-npu2
Runtime shared libraries for the XRT NPU path (Debian libxrt-npu2).

%package -n libxrt-alveo2
Summary:        Xilinx Runtime (XRT) ALVEO - runtime libraries

%description -n libxrt-alveo2
Runtime shared libraries for the XRT Alveo path, including scheduling and
(on x86_64) hardware/software emulation support (Debian libxrt-alveo2).

%package -n python3-xrt
Summary:        Xilinx Runtime (XRT) - Python bindings
Requires:       python3%{?_isa}
Requires:       libxrt2%{?_isa} = %{epoch}:%{version}-%{release}

%description -n python3-xrt
Python bindings for XRT (Debian python3-xrt).

%package -n libxrt-devel
Summary:        Xilinx Runtime (XRT) - development files
Requires:       python3-xrt%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       libxrt2%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       libxrt-npu2%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       libxrt-alveo2%{?_isa} = %{epoch}:%{version}-%{release}

%description -n libxrt-devel
Headers, CMake package files, pkg-config files, and static libraries
(Debian libxrt-dev).

%package -n libxrt-utils
Summary:        Xilinx Runtime (XRT) - utilities
Requires:       python3%{?_isa}

%description -n libxrt-utils
General-purpose XRT command-line tools (Debian libxrt-utils).

%package -n libxrt-utils-npu
Summary:        Xilinx Runtime (XRT) NPU - utilities
Requires:       libxrt-utils%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       libxrt-npu2%{?_isa} = %{epoch}:%{version}-%{release}

%description -n libxrt-utils-npu
NPU-specific utilities (Debian libxrt-utils-npu).

%package -n libxrt-utils-alveo
Summary:        Xilinx Runtime (XRT) ALVEO - utilities
Requires:       libxrt-utils%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       libxrt-alveo2%{?_isa} = %{epoch}:%{version}-%{release}

%description -n libxrt-utils-alveo
Alveo-specific utilities (Debian libxrt-utils-alveo).

%prep
%setup -q -n %{name}-%{version}

# Apply the same patch queue as Debian (src/debian/patches/series).
if [ -f debian/patches/series ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      ''|\#*) continue ;;
    esac
    echo "PATCH: debian/patches/${line}"
    /usr/bin/patch -p1 --fuzz=0 --silent -i debian/patches/${line}
  done < debian/patches/series
fi

# Apply patches specific to fedora
if [ -f fedora/patches/series ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      ''|\#*) continue ;;
    esac
    echo "PATCH: fedora/patches/${line}"
    /usr/bin/patch -p1 --fuzz=0 --silent -i fedora/patches/${line}
  done < fedora/patches/series
fi

%build
# Matches src/debian/rules CONFIGURE_ARGS; top-level CMake is this tree (see README).
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DXRT_NPU=1 \
  -DXRT_ALVEO=1 \
  -DCMAKE_BUILD_RPATH_USE_ORIGIN=ON \
  -DXRT_ENABLE_HIP=ON \
  -DXRT_ENABLE_TRACER=OFF \
  -DXRT_ENABLE_DKMS=OFF

%cmake_build

%install
%cmake_install

# --- Post-install steps from debian/rules (override_dh_auto_install) ---
# (Alveo emulation shlibs stay in %%{_libdir}; split vs libxrt2 is by %%files only.)

# xbtop: CMake installs the package under %%{_prefix}/python/ (see XRT_INSTALL_PYTHON_DIR
# in xrtVariables.cmake). Match debian/python3-xrt.install by placing _xbtop next to pyxrt.
if [ -d %{buildroot}%{_prefix}/python/_xbtop ]; then
  install -d %{buildroot}%{python3_sitearch}
  cp -a %{buildroot}%{_prefix}/python/_xbtop %{buildroot}%{python3_sitearch}/
  rm -rf %{buildroot}%{_prefix}/python/_xbtop
fi
rmdir %{buildroot}%{_prefix}/python 2>/dev/null || true

# Debian moves the installed Python entry script over the bin wrapper from CMake.
if [ -f %{buildroot}%{_prefix}/python/xbtop.py ]; then
  mv -f %{buildroot}%{_prefix}/python/xbtop.py %{buildroot}%{_bindir}/xbtop
elif [ -f %{buildroot}%{python3_sitearch}/xbtop.py ]; then
  mv -f %{buildroot}%{python3_sitearch}/xbtop.py %{buildroot}%{_bindir}/xbtop
fi

# debian/libxrt-utils-alveo.install: CMake installs xbflash2 under %%{_prefix}/local/bin; ship as %%{_bindir}/xbflash2.
# (Do not use %%{_localbindir}: it is not defined in Fedora's default macros and stays literal in the shell script.)
if [ -e %{buildroot}%{_prefix}/local/bin/xbflash2 ]; then
  install -d %{buildroot}%{_bindir}
  mv -f %{buildroot}%{_prefix}/local/bin/xbflash2 %{buildroot}%{_bindir}/xbflash2
fi
rmdir %{buildroot}%{_prefix}/local/bin %{buildroot}%{_prefix}/local 2>/dev/null || true

# Man pages shipped by Debian packaging (not always installed by upstream CMake).
install -d %{buildroot}%{_mandir}/man1
for m in xrt-replay.1 xclbinutil.1 aiebu-asm.1 aiebu-dump.1 xbflash2.1 xbflash.qspi.1 xbmgmt.1; do
  if [ -f debian/man/"$m" ]; then
    install -m 0644 debian/man/"$m" %{buildroot}%{_mandir}/man1/
  fi
done

# Bash completion (debian/libxrt-utils*.bash-completion).
install -d %{buildroot}%{_datadir}/bash-completion/completions
if [ -f %{buildroot}%{_datadir}/completions/xbutil-bash-completion ]; then
  install -m 0644 %{buildroot}%{_datadir}/completions/xbutil-bash-completion \
    %{buildroot}%{_datadir}/bash-completion/completions/xrt-smi
fi
if [ -f %{buildroot}%{_datadir}/completions/xbmgmt-bash-completion ]; then
  install -m 0644 %{buildroot}%{_datadir}/completions/xbmgmt-bash-completion \
    %{buildroot}%{_datadir}/bash-completion/completions/xbmgmt2
fi

# debian/not-installed: do not ship these upstream doc snippets in the packages.
rm -f %{buildroot}%{_datadir}/doc/CHANGELOG.rst %{buildroot}%{_datadir}/doc/CONTRIBUTING.rst 2>/dev/null || :

# ---------------------------------------------------------------------------
# Match debian/not-installed: remove paths upstream installs but no subpackage
# lists, so rpmbuild check-files does not fail on orphans.
# (Run after copying completions out of %%{_datadir}/completions/.)
# ---------------------------------------------------------------------------
rm -rf %{buildroot}/bins
# rm -rf %{buildroot}/usr/bin/*.sh
find %{buildroot}/usr/bin -mindepth 1 -maxdepth 1 -type f -name '*.sh' -delete
rm -rf %{buildroot}/usr/bin/mpd
rm -rf %{buildroot}/usr/bin/msd
#rm -rf %{buildroot}/usr/etc/*.service
find %{buildroot}/usr/etc -mindepth 1 -maxdepth 1 -type f -name '*.service' -delete
rm -rf %{buildroot}/usr/etc/nagios-plugins
#rm -rf %{buildroot}/usr/include/m*d_plugin.h
find %{buildroot}/usr/include -mindepth 1 -maxdepth 1 -type f -name 'm*d_plugin.h' -delete
#rm -rf %{buildroot}/usr/%{_lib}/libaws*.so*
find %{buildroot}/usr/%{_lib} -mindepth 1 -maxdepth 1 -type f -name 'libaws*.so*' -delete
#rm -rf %{buildroot}/usr/%{_lib}/libazure*.so*
find %{buildroot}/usr/%{_lib} -mindepth 1 -maxdepth 1 -type f -name 'libazure*.so*' -delete
#rm -rf %{buildroot}/usr/%{_lib}/libcontainer*.so*
find %{buildroot}/usr/%{_lib} -mindepth 1 -maxdepth 1 -type f -name 'libcontainer*.so*' -delete
#rm -rf %{buildroot}/usr/%{_lib}/libsched*.so
find %{buildroot}/usr/%{_lib} -mindepth 1 -maxdepth 1 -type f -name 'libsched*.so' -delete
rm -rf %{buildroot}/usr/license/LICENSE
rm -rf %{buildroot}/usr/local/bin/xbflash
rm -rf %{buildroot}/usr/share/completions/*
rm -rf %{buildroot}/usr/share/doc/CHANGELOG.rst
rm -rf %{buildroot}/usr/share/doc/CONTRIBUTING.rst
rm -rf %{buildroot}/usr/version.json

# not-installed also lists these at the fake install root; remove if present.
rm -rf %{buildroot}/.clang-tidy
rm -rf %{buildroot}/CMake
rm -rf %{buildroot}/include
rm -rf %{buildroot}/platform
rm -rf %{buildroot}/python
rm -rf %{buildroot}/runtime_src

%check
# debian/rules stages an install before tests; %%cmake_install already ran.
# Uncomment when CTest is reliable in mock/Koji:
# %ctest

%files
%license xrt/XRT/LICENSE

%files -n libxrt2
%{_libdir}/libxilinxopencl.so.*
%{_libdir}/libxrt++.so.*
%{_libdir}/libxrt_core.so.*
%{_libdir}/libxrt_coreutil.so.*
%{_libdir}/libxrt_hip.so.*
%{_datadir}/doc/NOTICE

%files -n libxrt-npu2
%{_libdir}/libxrt_driver_xdna.so.*
%{_libdir}/libxdp*.so.*
%{_libdir}/xrt/*/libxdp*.so.*

%files -n libxrt-alveo2
%{_libdir}/libsched_em*.so.*
%ifarch x86_64
%{_libdir}/libxrt_hwemu*.so.*
%{_libdir}/libxrt_swemu*.so.*
%{_libdir}/libxrt_noop.so.*
%endif

%files -n python3-xrt
%{python3_sitearch}/pyxrt*.so
%{python3_sitearch}/_xbtop/
%{_bindir}/xbtop

%files -n libxrt-devel
%{_includedir}/aiebu/*
%{_includedir}/xrt/*
%{_includedir}/CL/*
%{_includedir}/hip/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
# Unversioned "namelink" symlinks only (matches *.so, not *.so.N[.M...] runtime SONAMEs).
# Avoid listing each library: some (e.g. libxrt_driver_xdna) may have no .so link, only .so.*.
%{_libdir}/*.so
%{_datadir}/cmake/*

%files -n libxrt-utils
%{_bindir}/xrt-smi
%{_bindir}/xclbinutil
%{_sysconfdir}/OpenCL/vendors/*.icd
%{_mandir}/man1/xrt-replay.1*
%{_mandir}/man1/xclbinutil.1*
%{_datadir}/bash-completion/completions/xrt-smi

%files -n libxrt-utils-npu
%{_bindir}/xrt-runner
%{_bindir}/aiebu-*
%{_mandir}/man1/aiebu-asm.1*
%{_mandir}/man1/aiebu-dump.1*

%files -n libxrt-utils-alveo
%{_bindir}/xbflash.qspi
%{_bindir}/xbmgmt
%{_bindir}/xbflash2
%{_mandir}/man1/xbflash2.1*
%{_mandir}/man1/xbflash.qspi.1*
%{_mandir}/man1/xbmgmt.1*
%{_datadir}/bash-completion/completions/xbmgmt2

%changelog
* Wed Apr 22 2026 XRT-DEBIAN Packaging <packaging@localhost> - 1:2.21.75-1
- Remove DKMS packaging
* Mon Apr 20 2026 XRT-DEBIAN Packaging <packaging@localhost> - 1:2.21.75-1
- Initial Fedora spec mirroring src/debian binary package split.
