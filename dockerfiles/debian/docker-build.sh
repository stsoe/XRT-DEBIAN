#!/bin/bash
# Script to build the Docker image for NPU builds
set -e
    
show_help() {
    cat << EOF
Usage: $0 [IMAGE_NAME] [DOCKERFILE]

Builds a Docker image for NPU builds.

Arguments:
  IMAGE_NAME     Docker image name with tag (default: debuild-debian_unstable)
  DOCKERFILE     Path to Dockerfile (default: debian_unstable.Dockerfile)

Options:
  -h, --help     Show this help message

Examples:
  $0 debuild-u2404 ubuntu_2404.Dockerfile
  $0 debuild-debian_unstable debian_unstable.Dockerfile

EOF
    exit 0
}


IMAGE_NAME="debuild-debian_unstable"
DOCKERFILE="debian_unstable.Dockerfile"

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
            DOCKERFILE="$2"
        fi
        ;;
esac

echo "Building Docker image: ${IMAGE_NAME}"
echo "Using Dockerfile: ${DOCKERFILE}"

docker build -t ${IMAGE_NAME} -f ${DOCKERFILE} .

echo ""
echo "Docker image built successfully!"
echo "To run the container, use:"
echo "  ./docker-run.sh"
