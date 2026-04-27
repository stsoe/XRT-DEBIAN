# SPDX-License-Identifier: Apache-2.0
# Spec layout mirrors src/debian/control and src/debian/rules.
Name:           xrt
Epoch:          0
Version:        2.21.75
Release:        1%{?dist}
Summary:        AMD Xilinx FPGA and ACAP runtime (XRT)

License:        Apache-2.0 AND MIT AND MIT-Khronos-old
URL:            https://github.com/Xilinx/XRT

Source0:       %{name}-%{version}.tar.xz

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
BuildRequires:  rocm-hip-devel

%description
This source package builds XRT runtime libraries split for core / NPU / Alveo,
Python bindings, development files, and utilities.

%package npu
Summary:        AMD Xilinx Runtime (XRT) - NPU runtime libraries
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description npu
Runtime shared libraries for the XRT NPU path.  Facilitates usage of
AMD Ryzen NPU through software APIs provided by XRT.

%package alveo
Summary:        AMD Xilinx Runtime (XRT) - Alveo runtime libraries
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description alveo
Runtime shared libraries for the XRT Alveo path, including scheduling and
(on x86_64) hardware/software emulation support. Facilitates usage of
AMD Xilinx Alveo through software APIs provided by XRT.

%package -n python3-xrt
Summary:        AMD Xilinx Runtime (XRT) - Python bindings
Requires:       python3%{?_isa}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description -n python3-xrt
Python bindings for XRT.  Facilitates control of AMD Ryzen NPU
and AMD Xilinx Alveo through Python.

%package devel
Summary:        AMD Xilinx Runtime (XRT) - development files
Requires:       python3-xrt%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-npu%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-alveo%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       opencl-headers
Requires:       rocm-hip-devel%{?_isa}

%description devel
Headers, CMake package files, pkg-config files, and link libraries.

%package utils
Summary:        AMD Xilinx Runtime (XRT) - utilities
Requires:       python3%{?_isa}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       ocl-icd

%description utils
General purpose XRT command-line tools.

%package utils-npu
Summary:        AMD Xilinx Runtime (XRT) - NPU utilities
Requires:       %{name}-utils%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-npu%{?_isa} = %{epoch}:%{version}-%{release}

%description utils-npu
NPU specific utilities for AMD Ryzen NPU including AIE binary utilities (AIEBU).

%package utils-alveo
Summary:        AMD Xilinx Runtime (XRT) - Alveo utilities
Requires:       %{name}-utils%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-alveo%{?_isa} = %{epoch}:%{version}-%{release}

%description utils-alveo
Alveo-specific utilities for AMD Xilinx Alveo.  Includes management and flash tools.

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
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DXRT_NPU=1 \
  -DXRT_ALVEO=1 \
  -DCMAKE_BUILD_RPATH_USE_ORIGIN=ON \
  -DXRT_ENABLE_HIP=ON \
  -DXRT_ENABLE_TRACER=OFF \
  -DXRT_ENABLE_DKMS=OFF \
  -DXRT_INSTALL_STATIC_LIBRARY=OFF

%cmake_build

%install
%cmake_install

# xbtop: CMake installs the package under %%{_prefix}/python/ (see XRT_INSTALL_PYTHON_DIR
# in xrtVariables.cmake).
if [ -d %{buildroot}%{_prefix}/python/_xbtop ]; then
  install -d %{buildroot}%{python3_sitearch}
  cp -a %{buildroot}%{_prefix}/python/_xbtop %{buildroot}%{python3_sitearch}/
  rm -rf %{buildroot}%{_prefix}/python/_xbtop
fi
rmdir %{buildroot}%{_prefix}/python 2>/dev/null || true

# Move the installed Python entry script over the bin wrapper from CMake.
if [ -f %{buildroot}%{_prefix}/python/xbtop.py ]; then
  mv -f %{buildroot}%{_prefix}/python/xbtop.py %{buildroot}%{_bindir}/xbtop
elif [ -f %{buildroot}%{python3_sitearch}/xbtop.py ]; then
  mv -f %{buildroot}%{python3_sitearch}/xbtop.py %{buildroot}%{_bindir}/xbtop
fi

# Fix permission of non-executable scripts (skip package __init__.py: not a script, keep 0644)
for script in \
    %{buildroot}%{_bindir}/xbtop \
    %{buildroot}%{python3_sitearch}/_xbtop/*.py ; do
  [[ -f "$script" ]] || continue
  [[ "$(basename "$script")" == __init__.py ]] && chmod 0644 "$script" && continue
  chmod 755 "$script"
done

# CMake installs xbflash2 under %%{_prefix}/local/bin; ship as %%{_bindir}/xbflash2.
if [ -e %{buildroot}%{_prefix}/local/bin/xbflash2 ]; then
  install -d %{buildroot}%{_bindir}
  mv -f %{buildroot}%{_prefix}/local/bin/xbflash2 %{buildroot}%{_bindir}/xbflash2
fi
rmdir %{buildroot}%{_prefix}/local/bin %{buildroot}%{_prefix}/local 2>/dev/null || true

# Man pages shipped by Debian packaging (not always installed by upstream CMake).
install -d %{buildroot}%{_mandir}/man1
for m in xclbinutil.1 aiebu-asm.1 aiebu-dump.1 xbflash2.1 xbflash.qspi.1 xbmgmt.1; do
  if [ -f debian/man/"$m" ]; then
    install -m 0644 debian/man/"$m" %{buildroot}%{_mandir}/man1/
  fi
done

# Bash completion
install -d %{buildroot}%{_datadir}/bash-completion/completions
if [ -f %{buildroot}%{_datadir}/completions/xbutil-bash-completion ]; then
  install -m 0644 %{buildroot}%{_datadir}/completions/xbutil-bash-completion \
    %{buildroot}%{_datadir}/bash-completion/completions/xrt-smi
fi
if [ -f %{buildroot}%{_datadir}/completions/xbmgmt-bash-completion ]; then
  install -m 0644 %{buildroot}%{_datadir}/completions/xbmgmt-bash-completion \
    %{buildroot}%{_datadir}/bash-completion/completions/xbmgmt2
fi

# ---------------------------------------------------------------------------
# Match debian/not-installed: remove paths upstream installs but no subpackage
# lists, so rpmbuild check-files does not fail on orphans.
# (Run after copying completions out of %%{_datadir}/completions/.)
# ---------------------------------------------------------------------------
rm -rf %{buildroot}/bins
find %{buildroot}%{_bindir} -mindepth 1 -maxdepth 1 -type f -name '*.sh' -delete
rm -rf %{buildroot}%{_bindir}/{mpd,msd}
rm -rf %{buildroot}/usr/etc
find %{buildroot}%{_includedir} -mindepth 1 -maxdepth 1 -name 'm*d_plugin.h' -delete
find %{buildroot}%{_libdir} -mindepth 1 -maxdepth 1 -name 'libaws*.so*' -delete
find %{buildroot}%{_libdir} -mindepth 1 -maxdepth 1 -name 'libazure*.so*' -delete
find %{buildroot}%{_libdir} -mindepth 1 -maxdepth 1 -name 'libcontainer*.so*' -delete
find %{buildroot}%{_libdir} -mindepth 1 -maxdepth 1 -name 'libsched*.so' -delete
rm -rf %{buildroot}/usr/license
rm -rf %{buildroot}/usr/share/doc
rm -rf %{buildroot}/usr/local
rm -rf %{buildroot}%{_datadir}/completions
rm -rf %{buildroot}%{_datadir}/doc
rm -rf %{buildroot}/usr/version.json

# not-installed also lists these at the fake install root; remove if present.
rm -rf %{buildroot}/.clang-tidy
rm -rf %{buildroot}/CMake
rm -rf %{buildroot}/include
rm -rf %{buildroot}/platform
rm -rf %{buildroot}/python
rm -rf %{buildroot}/runtime_src

%check
# Uncomment when CTest is reliable in mock/Koji:
# %%ctest

%files
%license xrt/XRT/LICENSE
%license xrt/XRT/NOTICE
%{_libdir}/libxilinxopencl.so.*
%{_libdir}/libxrt++.so.*
%{_libdir}/libxrt_core.so.*
%{_libdir}/libxrt_coreutil.so.*
%{_libdir}/libxrt_hip.so.*

%files npu
%{_libdir}/libxrt_driver_xdna.so.*
%{_libdir}/libxdp*.so.*
%dir %{_libdir}/xrt
%dir %{_libdir}/xrt/module
%{_libdir}/xrt/*/libxdp*.so.*

%files alveo
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

%files devel
%dir %{_includedir}/xrt
%{_includedir}/xrt/*
%{_includedir}/CL/*
%dir %{_includedir}/hip
%{_includedir}/hip/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%dir %{_datadir}/cmake/XRT
%{_datadir}/cmake/XRT/*

%files utils
%{_bindir}/xrt-smi
%{_bindir}/xclbinutil
%{_sysconfdir}/OpenCL/vendors/*.icd
%{_mandir}/man1/xclbinutil.1*
%{_datadir}/bash-completion/completions/xrt-smi

%files utils-npu
%{_bindir}/xrt-runner
%{_bindir}/aiebu-*
%{_mandir}/man1/aiebu-asm.1*
%{_mandir}/man1/aiebu-dump.1*

%files utils-alveo
%{_bindir}/xbflash.qspi
%{_bindir}/xbmgmt
%{_bindir}/xbflash2
%{_mandir}/man1/xbflash2.1*
%{_mandir}/man1/xbflash.qspi.1*
%{_mandir}/man1/xbmgmt.1*
%{_datadir}/bash-completion/completions/xbmgmt2

%changelog
* Mon Apr 20 2026 Fedora Packaging <stsoe@amd.com> - 0:2.21.75-1
- Initial Fedora spec mirroring src/debian binary package split.
