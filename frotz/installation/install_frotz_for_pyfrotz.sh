#!/bin/bash
echo On Linux Frotz is compiled during `pip install pyfrotz` into `~/.pyfrotz`.
echo But pyfrotz searches in `$LD_LIBRARY_PATH/python3.x/site-packages/frotz`.
echo You need to copy it there manually.

ls -la ~/.pyfrotz
python -m site
target_folder=$LD_LIBRARY_PATH/python3.>>>x<<</site-packages/frotz
mkdir -p $target_folder
cp ~/.pyfrotz/dfrotz $target_folder
ls -la $target_folder
