#!/bin/bash

# failure is a natural part of life
set -e

# Log in to dockerhub
docker login -u jameslamb

# Build the container
docker build -t jameslamb/oss_report:$(cat VERSION) -f ui/Dockerfile-app ui/. --no-cache

# Push to dockerhub
docker push jameslamb/oss_report

echo "Pushed to dockerhub. Have a great day."
