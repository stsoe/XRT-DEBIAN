#!/bin/bash
# Script to run the Docker container for NPU debian build

set -e

show_help() {
    cat << EOF
Usage: $0 [IMAGE_NAME] [CONTAINER_NAME]

Run Docker container for NPU builds.

Arguments:
  IMAGE_NAME     Docker image name with tag (default: debuild-debian_unstable)
  CONTAINER_NAME Name of contaioner to create (default: debuild-debian-dev)

Options:
  -h, --help     Show this help message

Examples:
  $0 debuild-u2404 debuild-u2404-dev
  $0 debuild-debian_unstable debuild-debian-dev

EOF
    exit 0
}

IMAGE_NAME="debuild-debian_unstable"
CONTAINER_NAME="debuild-debian-dev"

# Parse arguments
case "$1" in
    -h|--help)
        show_help
        ;;
    "")
        # No arguments, use defaults
        ;;
    *)
        IMAGE_NAME="$1"
        if [[ -n "$2" ]]; then
            CONTAINER_NAME="$2"
        fi
        ;;
esac

# Get the directory where this script is located (TheRock root)
SCRIPT_DIR=$(readlink -f $(dirname ${BASH_SOURCE[0]}))
ROOT_DIR=$(readlink -f $SCRIPT_DIR/..)

# Check if container already exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container ${CONTAINER_NAME} already exists."
    echo "Starting existing container..."
    docker start -ai ${CONTAINER_NAME}
else
    echo "Creating new container: ${CONTAINER_NAME}"
    echo "Mounting XRT-DEBIAN repository from: ${ROOT_DIR}"
    echo ""
    echo "Inside the container, XRT-DEBIAN will be at: /workspace/XRT-DEBIAN"
    echo ""
    
    docker run -it \
        --name ${CONTAINER_NAME} \
        --hostname xrt-debian-build \
        -v "${ROOT_DIR}:/workspace/XRT-DEBIAN" \
        -w /workspace/XRT-DEBIAN \
        ${IMAGE_NAME} \
        /bin/bash
fi

echo ""
echo "To remove the container later, run:"
echo "  docker rm ${CONTAINER_NAME}"
echo ""
echo "To remove the image, run:"
echo "  docker rmi ${IMAGE_NAME}"
