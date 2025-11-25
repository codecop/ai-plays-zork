#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
pip freeze | cut -d'@' -f1 | xargs -r pip uninstall -y
pip list
