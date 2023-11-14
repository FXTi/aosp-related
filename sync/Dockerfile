# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Modify the APT sources list and install necessary packages
RUN apt-get update && \
    apt-get install -y curl git python3 python-is-python3 gnupg && \
    rm -rf /var/lib/apt/lists/*

# Set the REPO_URL environment variable and download and install the repo tool
ENV REPO_URL 'https://mirrors.tuna.tsinghua.edu.cn/git/git-repo'
RUN curl $REPO_URL -o /repo && \
    chmod a+x /repo && \
    git config --global http.postBuffer 524288000

# Update the PATH environment variable
ENV PATH /:$PATH

COPY every /usr/bin/every
RUN chmod 755 /usr/bin/every

RUN groupadd -g 3001 user && \
    useradd -u 3001 -g 3001 -m user

USER user
WORKDIR /aosp

# Run the entrypoint script on container startup
CMD ["every", "24h", "repo", "sync"]
