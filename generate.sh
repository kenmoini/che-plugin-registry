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

./build.sh -t ${TAG} -o ${ORG} --offline && podman push quay.io/${ORG}/pluginregistry-rhel9:${TAG}
