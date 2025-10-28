#!/bin/bash

SCRIPT_DIR=$(dirname "$0" | tr -d '\r')
"$SCRIPT_DIR/send_command.sh" "quit"
"$SCRIPT_DIR/send_command.sh" "Y"
