# % docker build -t xrt-debian-unstable -f dockerfiles/debian_unstable.Dockerfile .

FROM debian:unstable

ENV DEBIAN_FRONTEND=noninteractive

# Enable or add deb-src lines, then update
RUN set -e; \
    # 1) Uncomment existing deb-src lines if they are present but commented
    if grep -q '^#\s*deb-src ' /etc/apt/sources.list; then \
        sed -i 's/^#\s*deb-src /deb-src /' /etc/apt/sources.list; \
    fi; \
    # 2) Ensure the specific deb-src lines you want exist (append if not present)
    grep -q 'deb-src http://deb.debian.org/debian bookworm main contrib non-free-firmware' /etc/apt/sources.list \
      || echo 'deb-src http://deb.debian.org/debian bookworm main contrib non-free-firmware' >> /etc/apt/sources.list; \
    grep -q 'deb-src http://security.debian.org/debian-security bookworm-security main' /etc/apt/sources.list \
      || echo 'deb-src http://security.debian.org/debian-security bookworm-security main' >> /etc/apt/sources.list; \
    # 3) Update apt indexes
    apt-get update; \
    # Optional: clean apt cache to keep image small
    rm -rf /var/lib/apt/lists/*

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
    systemtap-sdt-dev

# Configure git to trust all directories (needed for version detection in containers)
RUN git config --global --add safe.directory '*'

# Default command
CMD ["/bin/bash"]
