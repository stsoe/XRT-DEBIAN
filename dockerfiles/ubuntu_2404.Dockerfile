# % docker build -t debuild-u2404 -f ubuntu_2404.Dockerfile .
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e; \
    sed -i 's|^Types: deb|Types: deb deb-src|' /etc/apt/sources.list.d/ubuntu.sources; \
    apt-get update; \
    rm -rf /var/lib/apt/lists/*

# NO DEBIAN BOOKWORM REPOS NEEDED - Ubuntu 24.04 has everything you need
# Install all build dependencies from Ubuntu 24.04 repos
RUN apt-get update && \
    apt-get install -y \
        tzdata \
        sudo \
        rsync \
        build-essential \
        fakeroot \
        devscripts \
        bash-completion \
        dh-python \
        help2man \
        systemtap-sdt-dev \
        quilt

# Configure git to trust all directories (needed for version detection in containers)
RUN git config --global --add safe.directory '*'

# Default command
CMD ["/bin/bash"]
