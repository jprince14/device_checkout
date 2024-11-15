#!/bin/bash

if [ -d "venv" ]; then
  rm -rf venv
fi
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 src/create_empty_database.py

docker compose build
docker compose create
