#!/bin/sh

echo "Entering Django project directory"
cd cruxOptimWebApp
echo "Installing bower dependencies for the Django project"
bower install
echo "Launching docker-compose"
cd ..
docker-compose -f docker-compose.development.yml up -d