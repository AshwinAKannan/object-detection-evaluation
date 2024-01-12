#!/bin/bash

USERNAME=$(whoami)

docker build --build-arg USERNAME=$USERNAME -t engine_image -f engine.Dockerfile .