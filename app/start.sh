#!/bin/bash
cd /home/loic/sdl/app

sudo tailscale funnel 8080 &

# Run the app
exec pipenv run python3 main.py
