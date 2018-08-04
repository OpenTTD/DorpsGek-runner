#!/bin/sh

echo "Running flake8 ..."
flake8 dorpsgek_runner

echo "Running test build for Docker image ..."
docker build --pull --no-cache --force-rm -t dorpsgek/runner:testrun . \
    && docker rmi dorpsgek/runner:testrun
