#!/bin/bash

SCRIPT_DIR=$(dirname "$0" | tr -d '\r')
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

MAP_NAME="map.txt"
MAP_PATH=$PROJECT_DIR/runs/$MAP_NAME

rm -f "$MAP_PATH"
