#!/bin/bash

echo "Pullin new GH version"
git pull origin main

echo "Building new container"
docker-compose build --no-cache
docker-compose up -d