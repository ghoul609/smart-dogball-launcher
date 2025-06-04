#!/bin/bash

sleep 10

cd /home/loic/sdl/app

sudo tailscale funnel 8080 &

# Run the app
exec python3 main.py
