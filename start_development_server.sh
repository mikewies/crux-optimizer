#!/bin/sh

echo "Entering Django project directory"
cd cruxOptimWebApp
echo "Installing bower dependencies"
bower install
echo "Launching docker-compose"
docker-compose -f docker-compose.development.yml up -d