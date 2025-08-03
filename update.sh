#!/bin/bash

docker compose down

git pull --rebase

docker build -t w-bot .

docker compose up -d
