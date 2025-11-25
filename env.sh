#!/usr/bin/env bash
set -euo pipefail

sourced=0
if [[ -n "${BASH_SOURCE[0]:-}" && "${BASH_SOURCE[0]}" != "${0}" ]]; then
    sourced=1
elif [[ -n "${ZSH_VERSION:-}" ]]; then
    [[ "$ZSH_EVAL_CONTEXT" =~ :file$ ]] && sourced=1
fi
if [[ "$sourced" -eq 0 ]]; then
    echo "This script must be sourced: source env.sh" >&2
    exit 1
fi

# TODO set up Frotz, copy dfrotz
ls -la ~/.pyfrotz
python -m site
target_folder=$LD_LIBRARY_PATH/python3.12/site-packages/frotz
mkdir -p $target_folder
cp ~/.pyfrotz/dfrotz $target_folder
ls -la $target_folder

# set up Python
if ! command -v python &>/dev/null; then
    echo "python not found in PATH" >&2
    exit 1
fi
python --version

# set up virtual environment
if [[ ! -d .venv ]]; then
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

pip list
