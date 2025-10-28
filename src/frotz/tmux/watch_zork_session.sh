#!/bin/bash

SCRIPT_DIR=$(dirname "$0" | tr -d '\r')
watch -n 1 "$SCRIPT_DIR/get_last_response.sh"
