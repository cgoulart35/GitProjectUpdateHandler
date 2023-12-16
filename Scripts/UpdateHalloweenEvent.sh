#!/bin/sh

cd ~/Code/HalloweenEvent

cp ~/Code/GitProjectUpdateHandler/Shared/HalloweenEvent/serviceAccountKey.json ~/Code/HalloweenEvent/
cp ~/Code/GitProjectUpdateHandler/Shared/HalloweenEvent/api.env ~/Code/HalloweenEvent/api.env
cp ~/Code/GitProjectUpdateHandler/Shared/HalloweenEvent/app.env ~/Code/HalloweenEvent/app.env

chmod -R 777 ~/Code/HalloweenEvent

docker compose -f docker-compose-prod.yml down
docker compose -f docker-compose-prod.yml up -d --build