#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No mount path provided. Usage: ./run.sh <mount_path>"
    exit 1
fi

mount_path=$1

cmd="docker run  \
    --network="host" \
    -it \
    --rm \
    -e DISPLAY=${DISPLAY} \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --name engine_v1 \
    -e HOST_USERNAME=$(whoami) \
    -v $mount_path:/work \
    engine_image /bin/bash"

echo "$cmd"
eval "$cmd"

