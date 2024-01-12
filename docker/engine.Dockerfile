FROM ubuntu:20.04
LABEL maintainer="ashwin.kannan3@gmail.com"

RUN apt-get update && apt-get install -y sudo

ARG USERNAME=default_user

RUN useradd -m -s /bin/bash ${USERNAME} && usermod -aG sudo ${USERNAME}

ARG DEBIAN_FRONTEND=noninteractive

# RUN apt-get update && apt-get upgrade -y
# Run package updates and install packages
RUN apt-get update \
    && apt-get -y install build-essential libssl-dev libffi-dev \
    && apt-get -y install libxml2-dev libxslt1-dev zlib1g-dev

RUN apt-get install -y wget
RUN apt-get install -y git
RUN apt-get install -y cmake
RUN apt-get install -y g++
RUN apt-get install -y gdb
RUN apt-get install -y python3.6
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-pip

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install fiftyone
RUN pip3 install dvc
RUN pip3 install pytest

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

USER ${USERNAME}

ENTRYPOINT ["/entrypoint.sh"]
