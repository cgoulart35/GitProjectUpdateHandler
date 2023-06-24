#!/bin/sh

cd ~/Code/GBot
cp ~/Code/GitProjectUpdateHandler/Shared/GBot/serviceAccountKey.json ~/Code/GBot/Shared/

# update prod instance

cp ~/Code/GitProjectUpdateHandler/Shared/GBot/gbot.env.prod ~/Code/GBot/Shared/gbot.env
chmod -R 777 ~/Code/GBot

docker compose -f docker-compose-prod.yml -p gbotprod01 down
docker compose -f docker-compose-prod.yml -p gbotprod01 up -d --build

# update dev instance

cp ~/Code/GitProjectUpdateHandler/Shared/GBot/gbot.env.dev ~/Code/GBot/Shared/gbot.env
chmod -R 777 ~/Code/GBot

docker compose -f docker-compose-dev.yml -p gbotdev01 down
docker compose -f docker-compose-dev.yml -p gbotdev01 up -d --build