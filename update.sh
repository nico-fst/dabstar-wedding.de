#!/bin/bash

echo "Pullin new GH version"
git pull origin main

echo "Stopping and removing old container"
docker-compose down

echo "Building new container"
docker-compose build --no-cache
docker-compose up -d