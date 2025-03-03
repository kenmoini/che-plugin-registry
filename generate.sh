#!/bin/bash

#set -x
VERSION="3.18"
ORG="kenmoini"
TAG="${VERSION}"

SCRIPT_DIR=$(pwd)

rm -rf /tmp/che-plugin-registry
mkdir -p /tmp/che-plugin-registry

git clone -b devspaces-${VERSION}-rhel-9 --depth=1 https://github.com/redhat-developer/devspaces /tmp/che-plugin-registry/devspaces

python3 ${SCRIPT_DIR}/generate-mirror-json.py -o /tmp/che-plugin-registry/devspaces/dependencies/che-plugin-registry/openvsx-sync.json

cd /tmp/che-plugin-registry/devspaces/dependencies/che-plugin-registry/

# Ignore prerelease exclusions causing failures to build - some extensions don't ever remove the pre-release flag
sed -i 's|$preRelease == true|$preRelease == "nottrue"|g' build/scripts/download_vsix.sh

# Stop buggy extensions with poor deps from failing 
# - vscode.github-authentication
# - redhat.vscode-yaml
# - redhat.java (????)
sed -i 's|set -e||g' build/scripts/import_vsix.sh
sed -i 's|set -o pipefail||g' build/scripts/import_vsix.sh

./build.sh -t ${TAG} -o ${ORG} --offline && podman push quay.io/${ORG}/pluginregistry-rhel9:${TAG}
