# Fedora image for rpmbuild of XRT (see dockerfiles/fedora/build-fed.sh).
#
# Build from this directory:
#   cd dockerfiles/fedora && ./docker-build.sh
# Or explicitly:
#   docker build -t rpmbuild-fedora-xrt:44 -f Dockerfile .

ARG FEDORA_VERSION=44
FROM fedora:${FEDORA_VERSION}

RUN dnf -y upgrade --refresh \
    && dnf -y install \
        ccache \
        cpio \
        dnf-plugins-core \
        git \
        gzip \
        make \
        patch \
        rpm-build \
        rpmdevtools \
        rsync \
        tar \
        xz \
    && dnf clean all

# rpmbuild tree (build-fed.sh also uses this layout)
RUN rpmdev-setuptree

RUN git config --global --add safe.directory '*'

WORKDIR /workspace

CMD ["/bin/bash"]
