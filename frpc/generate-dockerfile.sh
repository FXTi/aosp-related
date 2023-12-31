#!/bin/bash

# Get latest release tag from GitHub
tag_name=$(curl -s https://api.github.com/repos/fatedier/frp/releases/latest | jq -r ".tag_name")

# Create Dockerfile
cat << EOF > Dockerfile
FROM fatedier/frpc:$tag_name
EOF
