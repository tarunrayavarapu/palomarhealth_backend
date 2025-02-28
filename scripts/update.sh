#!/bin/bash

docker-compose down

git pull

source venv/bin/activate

python scripts/db_init_force.py

deactivate

docker-compose build

docker-compose up