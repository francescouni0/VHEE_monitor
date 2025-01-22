#!/usr/bin/env bash

for E in $(seq 50 250); do
    echo "Starting simulation with energy $E..."
    python gatevhee.py --energy "$E"
    echo "Simulation with energy $E completed."
done
