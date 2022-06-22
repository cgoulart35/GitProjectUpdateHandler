#!/bin/sh

cp ~/Code/GitProjectUpdateHandler/Shared/GBot/gbot.env ~/Code/GBot/Shared/
cp ~/Code/GitProjectUpdateHandler/Shared/GBot/serviceAccountKey.json ~/Code/GBot/Shared/

chmod -R 777 ~/Code/GBot

cd ~/Code/GBot

docker compose -f docker-compose-prod.yml down
docker compose -f docker-compose-prod.yml up -d --build