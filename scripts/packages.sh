#!/bin/bash

NEW_DOCKER_USER=$1

# setup packages
apt-get update
apt-get -y install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        wget \
        vim \
        sudo \
        software-properties-common \
        build-essential

# setup docker
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
apt-get update
apt-get -y install docker-ce docker-ce-cli containerd.io
usermod -aG docker $NEW_DOCKER_USER

# setup docker-compose
curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# setup tz
echo 'TZ="America/Los_Angeles"' >> /etc/environment

# setup docker directories
mkdir -p ./docker/portainer/data
mkdir -p ./docker/shared
