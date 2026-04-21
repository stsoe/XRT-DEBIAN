#!/bin/bash
# Run an interactive Fedora build container (same mount layout as docker-run.sh).
set -euo pipefail

show_help() {
  cat <<EOF
Usage: $0 [IMAGE_NAME] [CONTAINER_NAME]

Runs a container with this repository mounted at /workspace/XRT-DEBIAN.

Arguments:
  IMAGE_NAME       Docker image (default: rpmbuild-fedora-xrt:42)
  CONTAINER_NAME   Container name (default: rpmbuild-fedora-dev)

Options:
  -h, --help       Show this help message

Inside the container:
  ./dockerfiles/fedora/build-fed.sh

Example:
  $0 rpmbuild-fedora-xrt:42 my-fedora-build
EOF
  exit 0
}

case "${1:-}" in
  -h|--help) show_help ;;
esac

SCRIPT_DIR=$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")
ROOT_DIR=$(readlink -f "${SCRIPT_DIR}/../..")

IMAGE_NAME="${1:-rpmbuild-fedora-xrt:42}"
CONTAINER_NAME="${2:-rpmbuild-fedora-dev}"

if docker ps -a --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "Container ${CONTAINER_NAME} already exists; starting..."
  docker start -ai "${CONTAINER_NAME}"
else
  echo "Creating ${CONTAINER_NAME} from ${IMAGE_NAME}"
  echo "Mount: ${ROOT_DIR} -> /workspace/XRT-DEBIAN"
  docker run -it \
    --name "${CONTAINER_NAME}" \
    --hostname xrt-fedora-build \
    -v "${ROOT_DIR}:/workspace/XRT-DEBIAN" \
    -w /workspace/XRT-DEBIAN \
    "${IMAGE_NAME}" \
    /bin/bash
fi

echo ""
echo "Remove container: docker rm ${CONTAINER_NAME}"
echo "Remove image:     docker rmi ${IMAGE_NAME}"
