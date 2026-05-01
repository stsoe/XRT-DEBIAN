# SPDX-License-Identifier: Apache-2.0
# Spec layout mirrors src/debian/control and src/debian/rules.
# Assisted-by:    Generic LLM chatbot
Name:           xrt
Version:        2.21.75
Release:        1%{?dist}
Summary:        AMD Xilinx FPGA and ACAP runtime (XRT)

License:        Apache-2.0 AND MIT AND MIT-Khronos-old
URL:            https://github.com/Xilinx/XRT

# License breakdown:
# - Core XRT runtime: Apache-2.0
# - AIE binary utilities: MIT
# - Core XRT OpenCL library: Apache-2.0 and MIT-Khronos-old

Source0:        https://github.com/Xilinx/XRT/releases/download/%{version}/%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Debian patches
Patch0:         6.18.patch
Patch1:         6.19.patch
Patch2:         hip.patch
Patch3:         tracer.patch
Patch4:         hip2.patch
Patch5:         xrt-smi.patch
Patch6:         hip3.patch
Patch7:         xrt-9660.patch
Patch8:         xrt-9730.patch
Patch9:         xrt-9731.patch
Patch10:        xrt-9738.patch
Patch11:        xdna-1255.patch

# Fedora patches
Patch100:       dkms-disable.patch
Patch101:       static.patch
Patch102:       license.patch
Patch103:       xbmgmt-link.patch
Patch104:       emu-disable.patch

# Man pages not installed by CMake
Source10:       aiebu-asm.1
Source11:       aiebu-dump.1
Source12:       xbflash.qspi.1
Source13:       xbflash2.1
Source14:       xbmgmt.1
Source15:       xclbinutil.1
Source16:       xrt-replay.1

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
BuildRequires:  bash-completion

%description
AMD Xilinx Runtime (XRT) provides a runtime environment for AMD Xilinx
Alveo FPGAs and AMD Ryzen NPUs.  It includes core runtime
libraries, Python bindings, development files, and utilities for
managing and programming AMD Xilinx devices.

This package provides the core runtime environment for XRT.

%package npu
Summary:        AMD Xilinx Runtime (XRT) - NPU runtime libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description npu
AMD Xilinx Runtime (XRT) provides a runtime environment for AMD Xilinx
Alveo FPGAs and AMD Ryzen NPUs.  It includes core runtime
libraries, Python bindings, development files, and utilities for
managing and programming AMD Xilinx devices.

This package provides runtime shared libraries for the XRT NPU path.

%package -n python3-xrt
Summary:        AMD Xilinx Runtime (XRT) - Python bindings
Requires:       python3%{?_isa}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-xrt
AMD Xilinx Runtime (XRT) provides a runtime environment for AMD Xilinx
Alveo FPGAs and AMD Ryzen NPUs.  It includes core runtime
libraries, Python bindings, development files, and utilities for
managing and programming AMD Xilinx devices.

This package provides python bindings for XRT.

%package devel
Summary:        AMD Xilinx Runtime (XRT) - development files
Requires:       python3-xrt%{?_isa} = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-npu%{?_isa} = %{version}-%{release}
Requires:       libuuid-devel
Requires:       opencl-headers
Requires:       rocm-hip-devel%{?_isa}

%description devel
AMD Xilinx Runtime (XRT) provides a runtime environment for AMD Xilinx
Alveo FPGAs and AMD Ryzen NPUs.  It includes core runtime
libraries, Python bindings, development files, and utilities for
managing and programming AMD Xilinx devices.

This package provides development libraries and headers for %{name}

%package utils
Summary:        AMD Xilinx Runtime (XRT) - utilities
Requires:       python3%{?_isa}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       opencl-filesystem

%description utils
AMD Xilinx Runtime (XRT) provides a runtime environment for AMD Xilinx
Alveo FPGAs and AMD Ryzen NPUs.  It includes core runtime
libraries, Python bindings, development files, and utilities for
managing and programming AMD Xilinx devices.

This package provides general purpose XRT command-line tools.

%package utils-npu
Summary:        AMD Xilinx Runtime (XRT) - NPU utilities
Requires:       %{name}-utils%{?_isa} = %{version}-%{release}
Requires:       %{name}-npu%{?_isa} = %{version}-%{release}

%description utils-npu
AMD Xilinx Runtime (XRT) provides a runtime environment for AMD Xilinx
Alveo FPGAs and AMD Ryzen NPUs.  It includes core runtime
libraries, Python bindings, development files, and utilities for
managing and programming AMD Xilinx devices.

This package provides utilities for AMD Ryzen NPU including AIE binary
utilities (AIEBU).

%package utils-alveo
Summary:        AMD Xilinx Runtime (XRT) - Alveo utilities
Requires:       %{name}-utils%{?_isa} = %{version}-%{release}

%description utils-alveo
AMD Xilinx Runtime (XRT) provides a runtime environment for AMD Xilinx
Alveo FPGAs and AMD Ryzen NPUs.  It includes core runtime
libraries, Python bindings, development files, and utilities for
managing and programming AMD Xilinx devices.

This package provides utilities for AMD Xilinx Alveo including
management and flash tools.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DXRT_NPU=1 \
  -DXRT_ALVEO=1 \
  -DCMAKE_BUILD_RPATH_USE_ORIGIN=ON \
  -DXRT_ENABLE_HIP=ON \
  -DXRT_ENABLE_TRACER=OFF \
  -DXRT_ENABLE_DKMS=OFF \
  -DXRT_INSTALL_STATIC_LIBRARY=OFF \
  -DXRT_ENABLE_EMULATION=OFF

%cmake_build

%install
%cmake_install

# xbtop: CMake installs the package under %%{_prefix}/python/ (see XRT_INSTALL_PYTHON_DIR
# in xrtVariables.cmake).
# Move xbtop Python module to correct Fedora location
install -d -p %{buildroot}%{python3_sitearch}
mv %{buildroot}%{_prefix}/python/_xbtop %{buildroot}%{python3_sitearch}/
rmdir %{buildroot}%{_prefix}/python 2>/dev/null || :

# Move the installed Python entry script over the bin wrapper from CMake.
mv -f %{buildroot}%{_prefix}/python/xbtop.py %{buildroot}%{_bindir}/xbtop 2>/dev/null || :
mv -f %{buildroot}%{python3_sitearch}/xbtop.py %{buildroot}%{_bindir}/xbtop 2>/dev/null || :

# Fix python script permissions
chmod 755 %{buildroot}%{_bindir}/xbtop
chmod 755 %{buildroot}%{python3_sitearch}/_xbtop/*.py
chmod 644 %{buildroot}%{python3_sitearch}/_xbtop/__init__.py

# CMake installs xbflash2 under %%{_prefix}/local/bin; ship as %%{_bindir}/xbflash2.
mv -f %{buildroot}%{_prefix}/local/bin/xbflash2 %{buildroot}%{_bindir}/xbflash2
rmdir %{buildroot}%{_prefix}/local/bin %{buildroot}%{_prefix}/local 2>/dev/null || :

# Man pages, not installed by upstream CMake
install -d -m 0755 %{buildroot}%{_mandir}/man1
install -p -m 0644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} \
        %{SOURCE14} %{SOURCE15} %{buildroot}%{_mandir}/man1/

# Bash completion
# Upstream CMake puts in wrong location - move to correct path
install -d -m 0755 %{buildroot}%{bash_completions_dir}
install -Dpm 0644 %{buildroot}%{_datadir}/completions/xbutil-bash-completion \
   %{buildroot}%{bash_completions_dir}/xrt-smi || :
install -Dpm 0644 %{buildroot}%{_datadir}/completions/xbmgmt-bash-completion \
   %{buildroot}%{bash_completions_dir}/xbmgmt2 || :
rm -rf %{buildroot}%{_datadir}/completions 2>/dev/null || :

# ---------------------------------------------------------------------------
# Remove paths upstream installs but no subpackage lists, so rpmbuild
# check-files does not fail on orphans.
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
rm -rf %{buildroot}/.clang-tidy
rm -rf %{buildroot}/CMake
rm -rf %{buildroot}/include
rm -rf %{buildroot}/platform
rm -rf %{buildroot}/python
rm -rf %{buildroot}/runtime_src

%check
%ctest

%files
%license xrt/XRT/LICENSE
%license xrt/XRT/NOTICE
%doc xrt/XRT/README.rst
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

%files -n python3-xrt
%dir %{python3_sitearch}/_xbtop/
%{python3_sitearch}/pyxrt*.so
%{python3_sitearch}/_xbtop/*
%{_bindir}/xbtop

%files devel
%dir %{_includedir}/xrt
%{_includedir}/xrt/*
%{_includedir}/CL/*
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
* Mon Apr 20 2026 Fedora Packaging <stsoe@amd.com> - 2.21.75-1
- Initial Fedora spec mirroring src/debian binary package split.
