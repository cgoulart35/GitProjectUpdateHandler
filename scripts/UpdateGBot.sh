#!/bin/sh

cd ~/Code/GBot

docker-compose -f docker-compose-prod.yml down
docker-compose -f docker-compose-prod.yml up -d --build