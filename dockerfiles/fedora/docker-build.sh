#!/bin/bash
# Build the Fedora rpmbuild Docker image (run from anywhere).
set -euo pipefail

show_help() {
  cat <<EOF
Usage: $0 [IMAGE_NAME]

Builds the Fedora Docker image defined in this directory.

Arguments:
  IMAGE_NAME   Image name:tag (default: rpmbuild-fedora-xrt:42)

Environment:
  FEDORA_VERSION   Base Fedora release passed as Docker build-arg (default: 42)

Options:
  -h, --help     Show this help message

Example:
  $0
  $0 rpmbuild-fedora-xrt:rawhide
EOF
  exit 0
}

case "${1:-}" in
  -h|--help) show_help ;;
esac

SCRIPT_DIR=$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")
IMAGE_NAME="${1:-rpmbuild-fedora-xrt:42}"
FEDORA_VERSION="${FEDORA_VERSION:-42}"

echo "Building image: ${IMAGE_NAME} (FROM fedora:${FEDORA_VERSION})"
docker build \
  --build-arg "FEDORA_VERSION=${FEDORA_VERSION}" \
  -t "${IMAGE_NAME}" \
  -f "${SCRIPT_DIR}/Dockerfile" \
  "${SCRIPT_DIR}"

echo ""
echo "Image built: ${IMAGE_NAME}"
echo "Run an interactive shell with the repo mounted:"
echo "  ${SCRIPT_DIR}/docker-run-fed.sh ${IMAGE_NAME}"
