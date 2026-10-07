#!/bin/bash
set -euo pipefail

# Use the tag given as $1, otherwise look up the latest release tag from GitHub
tag_name="${1:-$(curl -fsSL https://api.github.com/repos/fatedier/frp/releases/latest | jq -r '.tag_name')}"
if [ -z "$tag_name" ] || [ "$tag_name" = "null" ]; then
  echo "Could not resolve the latest fatedier/frp release tag." >&2
  exit 1
fi

# Create Dockerfile
cat << EOF > Dockerfile
FROM fatedier/frpc:$tag_name
EOF
