#!/bin/sh

echo "Stopping and remove development containers"
docker-compose -f docker-compose.development.yml down