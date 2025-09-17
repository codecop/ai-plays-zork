#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
MAP_NAME="map.txt"
MAP_PATH=$PROJECT_DIR/runs/$MAP_NAME

# Check if commands provided
if [ -z "$3" ]; then
    echo "Usage: $0 \"FROM_ROOM\" \"DIRECTION_OR_ACTION\" \"TO_ROOM\""
    exit 1
fi

echo "\"$1\" \"$2\" \"$3\""  >> $MAP_PATH

mv $MAP_PATH $MAP_PATH.bak
sort --ignore-case $MAP_PATH.bak | uniq > $MAP_PATH

