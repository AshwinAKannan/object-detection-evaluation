#!/bin/bash
# create a new user if username is passed
if [ ! -z "$HOST_USERNAME" ]; then
    useradd -m $HOST_USERNAME
    cd /home/$HOST_USERNAME
else
    cd /home/
fi
exec "$@"