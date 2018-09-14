#!/bin/bash

# failure is a natural part of life
set -e

# where on dockerhub should we push to?
REPOSITORY=$1

# Log in to dockerhub
docker login -u ${REPOSITORY}

# Build the container
docker build -t ${REPOSITORY}/oss_report:$(cat VERSION) -f ui/Dockerfile-app ui/. --no-cache

# Push to dockerhub
docker push ${REPOSITORY}/oss_report

echo "Pushed to dockerhub. Have a great day."
