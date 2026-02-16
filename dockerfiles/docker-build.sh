#!/bin/bash
# Script to build the Docker image for NPU builds

set -e

IMAGE_NAME="xrt-debian-unstable-2"
DOCKERFILE="debian_unstable.Dockerfile"

echo "Building Docker image: ${IMAGE_NAME}"
echo "Using Dockerfile: ${DOCKERFILE}"

docker build -t ${IMAGE_NAME} -f ${DOCKERFILE} .

echo ""
echo "Docker image built successfully!"
echo "To run the container, use:"
echo "  ./docker-run.sh"
