#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
MAP_NAME="map.txt"
MAP_PATH=$PROJECT_DIR/runs/$MAP_NAME
rm -f $MAP_PATH