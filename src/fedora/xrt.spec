# SPDX-License-Identifier: MIT
%global xrt_major 2
%global xrt_minor 21
%global xrt_patch 75
%global xrt_release %{xrt_major}.%{xrt_minor}
%global xrt_version %{xrt_release}.%{xrt_patch}

Name:           xrt
Version:        2.21.75
Release:        %autorelease
Summary:        Run Time for AIE and FPGA based platforms

License:        Apache-2.0 AND MIT AND Khronos
URL:            https://github.com/Xilinx/XRT

# License breakdown:
# Files: *
# - License: Apache-2.0
#
# Files: xrt/XRT/src/runtime_src/xocl/api/khronos/check_copy_overlap.cpp
#        xrt-2.21.75-build/xrt-2.21.75/xrt/XRT/src/include/1_2/CL/cl_ext.h
#        xrt-2.21.75-build/xrt-2.21.75/xrt/XRT/src/include/1_2/CL/cl_ext_xilinx.h
# - License: Khronos
#
# Files: xrt/XRT/src/runtime_src/core/common/aie-rt/*
# - License: MIT
#
# Files: xrt/XRT/src/runtime_src/core/common/aiebu/*
# - License: MIT
#
# Files: xrt/XRT/src/runtime_src/core/common/elf/elfio/*
# - License: MIT
#
# Files: xrt/XRT/src/runtime_src/core/common/gsl
# - License: MIT
#
# Files: xrt/XRT/src/runtime_src/core/pcie/driver/linux/*
# - License: GPL-2
#
# Files: xrt/XRT/src/runtime_src/core/include/xclbin.h
#        xrt/XRT/src/runtime_src/core/include/xcl_graph.h
#        xrt/XRT/src/runtime_src/core/include/xrt/deprecated/xclerr.h
#        xrt/XRT/src/runtime_src/core/include/xrt/detail/ert.h
#        xrt/XRT/src/runtime_src/core/include/xrt/detail/xclbin.h
#        xrt/XRT/src/runtime_src/core/include/xrt/detail/xrt_error_code.h
#        xrt/XRT/src/runtime_src/core/include/xrt/detail/xrt_mem.h
# License: Apache-2.0 or GPL-2
#
# Files: xdna/xdna-driver/src/shim/virtio/amdxdna_proto.h
#        xdna/xdna-driver/src/shim/virtio/drm_hw.h
# - License: MIT

Source0:        https://github.com/Xilinx/XRT/releases/download/%{version}/%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Backport eventfd_signal() simplification from Linux v6.8 to v6.7 kernel module
# Linux commit 3652117f854819a148ff0fbe4492587d3520b5e5
# https://github.com/Xilinx/XRT/pull/9730
Patch0:         6.18.patch
# Restore legacy uppercase DRM log helpers removed in newer kernels
# https://github.com/Xilinx/XRT/pull/9672
Patch1:         6.19.patch
# Add missing <cstdint> include to core/common/utils.h for std::uint* types
# https://github.com/Xilinx/XRT/pull/9730
Patch2:         hip.patch
# Remove obsolete cmake version check for xbtracer subdirectory conditional
# https://github.com/Xilinx/XRT/pull/9730
Patch3:         tracer.patch
# Fix static initialization order and update copyright year in HIP device files
# https://github.com/Xilinx/XRT/pull/9730
Patch4:         hip2.patch
# Fix xrt-smi platform path lookup, message logging, and archive handling
# https://github.com/Xilinx/XRT/pull/9730
Patch5:         xrt-smi.patch
# Fix trailing whitespace and const-correctness in HIP memory API functions
# https://github.com/Xilinx/XRT/pull/9730
Patch6:         hip3.patch
# Add run buffer pool max-size config knob; fix pool memory cache logic
# https://github.com/Xilinx/XRT/pull/9657
Patch7:         xrt-9660.patch
# Add missing <cstring> include to core/common/message.cpp
# https://github.com/Xilinx/XRT/pull/9730
Patch8:         xrt-9730.patch
# Suppress GCC 16 -Warray-bounds warnings; fix strncpy off-by-one in HIP
# https://github.com/Xilinx/XRT/pull/9731
Patch9:         xrt-9731.patch
# Remove unused loop counters causing GCC warnings; update copyright years
# https://github.com/Xilinx/XRT/pull/9738
Patch10:        xrt-9738.patch
# Fix compilation errors with GCC 16 in XDNA UMQ debug hardware queue
# https://github.com/amd/xdna-driver/pull/1255
Patch11:        xdna-1255.patch
# Fix missing comma in pyxrt pybind11 method chain causing build error
# https://github.com/Xilinx/XRT/pull/9813
Patch12:        xrt-9813.patch
# Guard XDNA buffer mmap against null range address; fix physical address return
# https://github.com/amd/xdna-driver/pull/1333
Patch13:        xdna-1333.patch
# Remove unused XDNA UMQ AIE debug infrastructure files
# https://github.com/amd/xdna-driver/pull/1371
Patch14:        xdna-1371.patch
# Add bounds-checking to fix security vulnerability in xclbin AIE_PARTITION parsing
# https://github.com/Xilinx/XRT/pull/9848
Patch15:        xrt-9848.patch

# Add XRT_ENABLE_DKMS cmake option so DKMS can be disabled at configure time
# https://github.com/Xilinx/XRT/pull/9751
Patch100:       dkms-disable.patch
# Add XRT_INSTALL_STATIC_LIBRARY option; gate static lib installs behind it
# https://github.com/Xilinx/XRT/pull/9753
# https://github.com/Xilinx/aiebu/pull/276
Patch101:       static.patch
# License verbiage was fixed in upstream per review.txt.  This patch
# resolves rpmlint review and reflects changes made in upstream XRT
# https://github.com/Xilinx/XRT/pull/9753
Patch102:       license.patch
# Drop unused boost_system and boost filesystem link dependencies from xbmgmt2
Patch103:       xbmgmt-link.patch
# Add XRT_ENABLE_EMULATION cmake option to disable Alveo emulation libraries
# https://github.com/Xilinx/XRT/pull/9753
Patch104:       emu-disable.patch
# Call enable_testing() in top-level CMakeLists so ctest targets are registered
# https://github.com/Xilinx/XRT/pull/9768
Patch105:       enable-testing.patch
# Support RelWithDebInfo in AIEBU install configurations
# https://github.com/Xilinx/aiebu/pull/297
Patch106:       aiebu-297.patch

# Man pages not installed by CMake
Source10:       aiebu-asm.1
Source11:       aiebu-dump.1
Source12:       xbflash.qspi.1
Source13:       xbflash2.1
Source14:       xbmgmt.1
Source15:       xclbinutil.1

ExclusiveArch:  aarch64 x86_64

# Build toolchain
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig

# System/hardware libraries
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(ocl-icd)
BuildRequires:  opencl-headers
BuildRequires:  libuuid-devel
BuildRequires:  ncurses-devel
BuildRequires:  systemtap-sdt-devel

# C++ libraries
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(RapidJSON)
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-compiler
BuildRequires:  rocm-hip-devel

# Python bindings
BuildRequires:  python3-devel
BuildRequires:  python3-rpm-macros
BuildRequires:  pybind11-devel

# Documentation / packaging helpers
BuildRequires:  doxygen
BuildRequires:  bash-completion

%description
AMD Xilinx Runtime (XRT) provides a runtime environment for AMD Xilinx
Alveo FPGAs and AMD Ryzen NPUs.  It includes core runtime
libraries, Python bindings, development files, and utilities for
managing and programming AMD Xilinx devices.

This package provides the core runtime environment for XRT.

%package npu
Summary:        AMD Xilinx Runtime (XRT) - NPU runtime libraries
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description npu
AMD Xilinx Runtime (XRT) provides a runtime environment for AMD Xilinx
Alveo FPGAs and AMD Ryzen NPUs.  It includes core runtime
libraries, Python bindings, development files, and utilities for
managing and programming AMD Xilinx devices.

This package provides runtime shared libraries for the XRT NPU path.

%package -n python3-xrt
Summary:        AMD Xilinx Runtime (XRT) - Python bindings
License:        Apache-2.0
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

# Exclude unused code for easier license review
rm -rf debian
rm -rf xdna/xdna-driver/src/driver
rm -rf xdna/xdna-driver/src/shim_ve2
rm -rf xdna/xdna-driver/tools
rm -rf xrt/XRT/.clangd
rm -rf xrt/XRT/.github
rm -rf xrt/XRT/.travis.yml
rm -rf xrt/XRT/build
rm -rf xrt/XRT/pyrightconfig.json
rm -rf xrt/XRT/src/.clang-tidy
rm -rf xrt/XRT/src/platform
rm -rf xrt/XRT/src/runtime_src/aie-rt/driver/docs
rm -rf xrt/XRT/src/runtime_src/aie-rt/driver/tests
rm -rf xrt/XRT/src/runtime_src/aie-rt/fal
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/.github
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/build.gradle
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/gradle.properties
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/publish
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/pyrightconfig.json
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/settings.gradle
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/lib/aie-rt
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/.dir-locals.el
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/.clang-format
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/.github
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/.tipi/deps
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/.tipi/opts
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/.travis.yml
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/BUILD.bazel
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/CHANGELOG.md
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/INSTALL
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/README.md
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/WORKSPACE
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/packaging
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/src/.tipi
rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/test
rm -rf xrt/XRT/src/runtime_src/core/common/drv
rm -rf xrt/XRT/src/runtime_src/core/common/elf/.clang-format
rm -rf xrt/XRT/src/runtime_src/core/common/elf/.github
rm -rf xrt/XRT/src/runtime_src/core/common/elf/.vscode
rm -rf xrt/XRT/src/runtime_src/core/common/elf/CMakeLists.txt
rm -rf xrt/XRT/src/runtime_src/core/common/elf/cmake
rm -rf xrt/XRT/src/runtime_src/core/common/elf/doc
rm -rf xrt/XRT/src/runtime_src/core/common/elf/examples
rm -rf xrt/XRT/src/runtime_src/core/common/elf/tests
rm -rf xrt/XRT/src/runtime_src/core/common/runner/test
rm -rf xrt/XRT/src/runtime_src/core/edge
rm -rf xrt/XRT/src/runtime_src/core/pcie/driver/.dir-locals.el
rm -rf xrt/XRT/src/runtime_src/core/pcie/driver/aws
rm -rf xrt/XRT/src/runtime_src/core/pcie/driver/linux/xocl
rm -rf xrt/XRT/src/runtime_src/core/pcie/driver/windows
rm -rf xrt/XRT/src/runtime_src/core/pcie/emulation
rm -rf xrt/XRT/src/runtime_src/core/pcie/tools/README
rm -rf xrt/XRT/src/runtime_src/core/tools/xbtracer
rm -rf xrt/XRT/src/runtime_src/doc
rm -rf xrt/XRT/src/runtime_src/ert
rm -rf xrt/XRT/src/runtime_src/tools/scripts/apu_recipes
rm -rf xrt/XRT/src/runtime_src/tools/scripts/is_supported.json
rm -rf xrt/XRT/src/runtime_src/tools/scripts/pkgapu.sh
rm -rf xrt/XRT/src/runtime_src/tools/scripts/rtplot
rm -rf xrt/XRT/src/runtime_src/tools/xclbinutil/aie-pdi-transform/.clang-tidy
rm -rf xrt/XRT/src/runtime_src/tools/xclbinutil/unittests
rm -rf xrt/XRT/src/runtime_src/xrt/test
rm -rf xrt/XRT/tests

%build
%cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
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
mv -f %{buildroot}%{_prefix}/python/xbtop.py %{buildroot}%{_bindir}/xbtop 2>/dev/null || :
rmdir %{buildroot}%{_prefix}/python 2>/dev/null || :

# Move the installed Python entry script over the bin wrapper from CMake.
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

# Install bundled submodule license files with unique names to avoid collisions
install -d %{buildroot}%{_licensedir}/%{name}
install -pm 0644 xrt/XRT/LICENSE \
   %{buildroot}%{_licensedir}/%{name}/LICENSE.xrt
install -pm 0644 xrt/XRT/NOTICE \
   %{buildroot}%{_licensedir}/%{name}/NOTICE.xrt
install -pm 0644 xrt/XRT/src/runtime_src/core/common/aiebu/LICENSE \
   %{buildroot}%{_licensedir}/%{name}/LICENSE.aiebu
install -pm 0644 xrt/XRT/src/runtime_src/core/common/aiebu/NOTICE \
   %{buildroot}%{_licensedir}/%{name}/NOTICE.aiebu
install -pm 0644 xrt/XRT/src/runtime_src/core/common/elf/LICENSE.txt \
   %{buildroot}%{_licensedir}/%{name}/LICENSE.elf
install -pm 0644 xrt/XRT/src/runtime_src/core/common/gsl/LICENSE \
   %{buildroot}%{_licensedir}/%{name}/LICENSE.gsl
install -pm 0644 xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/LICENSE \
   %{buildroot}%{_licensedir}/%{name}/LICENSE.cxxopts
install -pm 0644 xrt/XRT/src/runtime_src/aie-rt/license.txt \
   %{buildroot}%{_licensedir}/%{name}/LICENSE.aie-rt
install -d %{buildroot}%{_licensedir}/%{name}-npu
install -pm 0644 xdna/xdna-driver/LICENSE.amdnpu \
   %{buildroot}%{_licensedir}/%{name}-npu/LICENSE.amdnpu

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
rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}/usr/local
rm -rf %{buildroot}/usr/version.json
rm -rf %{buildroot}/.clang-tidy
rm -rf %{buildroot}/CMake
rm -rf %{buildroot}/include
rm -rf %{buildroot}/platform
rm -rf %{buildroot}/python
rm -rf %{buildroot}/runtime_src

%check
XILINX_XRT=%{buildroot}/usr \
%{__ctest} --test-dir redhat-linux-build --output-on-failure --force-new-ctest-process -j%{?_smp_build_ncpus}


%files
%license %{_licensedir}/%{name}/*
%doc xrt/XRT/README.rst
%{_libdir}/libxilinxopencl.so.%{xrt_major}{,.*}
%{_libdir}/libxrt++.so.%{xrt_major}{,.*}
%{_libdir}/libxrt_core.so.%{xrt_major}{,.*}
%{_libdir}/libxrt_coreutil.so.%{xrt_major}{,.*}
%{_libdir}/libxrt_hip.so.%{xrt_major}{,.*}

%files npu
%license %{_licensedir}/%{name}-npu/*
%doc xdna/xdna-driver/README.md
%{_libdir}/libxrt_driver_xdna.so.%{xrt_major}{,.*}
%{_libdir}/libxdp*.so.%{xrt_major}{,.*}
%dir %{_libdir}/xrt
%dir %{_libdir}/xrt/module
%{_libdir}/xrt/*/libxdp*.so.%{xrt_major}{,.*}

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
%autochangelog
