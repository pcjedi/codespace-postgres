FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    git \
    sudo \ 
    python3-sqlalchemy \
    python3-psycopg2 \
    python3-pytest \
    jupyter \
    black \
    python3-flake8 && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoclean && \
    apt-get clean && \
    apt-get autoremove && \
    useradd -ms /bin/bash vscode && \
    echo '%vscode ALL=(root) NOPASSWD:ALL' > /etc/sudoers.d/vscode