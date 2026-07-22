#!/bin/sh

# Filter unused sources before creating source drop
# This script is shared between debian and fedora

find . -depth -type f -name .clangd -exec /bin/rm -rf {} \;
find . -depth -type f -name .clang-format -exec /bin/rm -rf {} \;
find . -depth -type f -name .clang-tidy -exec /bin/rm -rf {} \;
find . -depth -type f -name .dir-locals.el -exec /bin/rm -rf {} \;
find . -depth -type f -name .git -exec /bin/rm -rf {} \;
find . -depth -type f -name .gitattributes -exec /bin/rm -rf {} \;
find . -depth -type d -name .github -exec /bin/rm -rf {} \;
find . -depth -type f -name .gitignore -exec /bin/rm -rf {} \;
find . -depth -type f -name .gitmodules -exec /bin/rm -rf {} \;
find . -depth -type f -name .vscode -exec /bin/rm -rf {} \;
find . -depth -type d -name elf_examples -exec /bin/rm -rf {} \;
find . -depth -type f -name pyrightconfig.json -exec /bin/rm -rf {} \;
find . -depth -type f -name usertest -exec /bin/rm -rf {} \;
find . -depth -type f -name \*.elf -exec /bin/rm {} \;
find . -depth -type f -name \*.a -exec /bin/rm {} \;
find . -depth -type f -name \*.swn -exec /bin/rm {} \;
find . -depth -type f -name \*.swo -exec /bin/rm {} \;

/bin/rm -rf xdna/xdna-driver/xrt
/bin/rm -rf xdna/xdna-driver/src/driver
/bin/rm -rf xdna/xdna-driver/src/shim_ve2
/bin/rm -rf xdna/xdna-driver/tools/bins
/bin/rm -rf xdna/xdna-driver/tools

/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/build.gradle
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/gradle.properties
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/publish
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/settings.gradle
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/lib/aie-rt
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/ELFIO
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/.tipi/deps
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/.tipi/opts
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/.travis.yml
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/BUILD.bazel
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/CHANGELOG.md
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/INSTALL
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/README.md
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/WORKSPACE
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/packaging
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/src/.tipi
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/cxxopts/test

/bin/rm -rf xrt/XRT/src/runtime_src/core/common/elf/CMakeLists.txt
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/elf/cmake
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/elf/doc
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/elf/examples
/bin/rm -rf xrt/XRT/src/runtime_src/core/common/elf/tests

/bin/rm -rf xrt/XRT/src/runtime_src/core/common/runner/test

/bin/rm -rf xrt/XRT/src/runtime_src/core/edge

/bin/rm -rf xrt/XRT/src/runtime_src/core/pcie/driver/windows
/bin/rm -rf xrt/XRT/src/runtime_src/core/pcie/tools/README
/bin/rm -rf xrt/XRT/src/runtime_src/core/tools/xbtracer
/bin/rm -rf xrt/XRT/src/runtime_src/doc
/bin/rm -rf xrt/XRT/src/runtime_src/tools/scripts/apu_recipes
/bin/rm -rf xrt/XRT/src/runtime_src/tools/scripts/is_supported.json
/bin/rm -rf xrt/XRT/src/runtime_src/tools/scripts/pkgapu.sh
/bin/rm -rf xrt/XRT/src/runtime_src/tools/scripts/rtplot
/bin/rm -rf xrt/XRT/src/runtime_src/tools/xclbinutil/unittests
/bin/rm -rf xrt/XRT/src/runtime_src/xrt/test
/bin/rm -rf xrt/XRT/tests

