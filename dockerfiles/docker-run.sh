#!/bin/bash
# Script to run the Docker container for TheRock development

set -e

IMAGE_NAME="xrt-debian-unstable-2"
CONTAINER_NAME="xrt-upstream-dev"

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
