#!/bin/bash
echo on Linux Frotz is compiled during `pip install` into `~/.pyfrotz`
echo but pyfrotz searches in `$LD_LIBRARY_PATH/python3.x/site-packages/frotz`
echo you need to copy it there

ls -la ~/.pyfrotz
python -m site
target_folder=$LD_LIBRARY_PATH/python3.x/site-packages/frotz
echo $target_folder
mkdir -p $target_folder
cp ~/.pyfrotz/dfrotz $target_folder
ls -la $target_folder
