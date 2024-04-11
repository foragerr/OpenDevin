FROM ubuntu:22.04

# install basic packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    unzip \
    zip \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    openssh-server \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_20.x | bash && \
    apt-get install -y nodejs && \
    pip3 install flake8 && \
    npm install -g eslint

RUN service ssh start
