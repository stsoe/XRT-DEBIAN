# XRT-DEBIAN
Local repo for debian upstreaming

## Build 

### Prepare docker image

Build a docker image for debian-unstable

```
% cd <>/debian-unstable
% sudo docker build -t xrt-debian-unstable .
```

Install packages for building using debuild.

```
% sudo apt update
% sudo apt-get install build-essential fakeroot devscripts
```

Edit or create /etc/apt/sources.list 

```
% sudo <edit> /etc/apt/sources.list
# add these files
deb-src http://deb.debian.org/debian bookworm main contrib non-free-firmware
deb-src http://security.debian.org/debian-security bookworm-security main

% sudo apt update
```

Install build dependencies declared in the package's debian/control by running:

```
% sudo apt-get build-dep xrt
```

### Prepare the build sources

Update the submodules to reflect the release we are building. The copy all
sources to /tmp 

```
% mkdir /tmp/upstream/<version>
% rsync -avz . /tmp/upstream/<version>/
```

Trim the copied sources to reflect the sources that will be
bundled into a source drop.

```
% cd /tmp/upstream/<version>
% /bin/rm -rf xdna/xdna-driver/xrt; /bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/src/cpp/ELFIO; /bin/rm -rf xrt/XRT/src/runtime_src/core/common/aiebu/lib/aie-rt; find . -type f -name .git -exec /bin/rm -rf {} \; ; find . -type d -name elf_examples -exec /bin/rm -rf {} \; ;find . -type f -name usertest -exec /bin/rm -rf {} \; ;find . -type f -name \*.elf -exec /bin/rm {} \; ;/bin/rm -rf xdna/xdna-driver/tools/bins
```

### Build

It's possible debuild will request additional package install, for example 
I had to install these after first attempt at debuild

```
% sudo apt install bash-completion dh-python help2man systemtap-sdt-dev
```

Now run

```
% debuild -us -uc |& tee ~/tmp/debuild.log.<version>.1
```








