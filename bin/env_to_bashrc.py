#!/usr/bin/env python

import os
import re


def normalize_path(path):
    return (
        path.replace("\\", "/")
        .replace("/Program Files/", "/Progra~1/")
        .replace("/Program Files (x86)/", "/Progra~2/")
        .replace(" ", "\\ ")
    )


def convert_path(path):
    if re.match(r"^[A-Za-z]:", path):
        drive = path[0].lower()
        rest = normalize_path(path[2:])
        converted = f"/cygdrive/{drive}{rest}"
    else:
        converted = normalize_path(path)
    # if " " in converted:
    #     converted = f'"{converted}"'
    return converted


def convert_path_list(value):
    converted_paths = [convert_path(path) for path in value.split(";")]
    return ":".join(converted_paths)


def is_path_variable(value):
    return ";" in value and ("\\" in value or ":" in value)


def convert_value(value):
    if is_path_variable(value):
        return convert_path_list(value)
    return convert_path(value)


def generate_bashrc(output_file="bashrc"):
    env_vars = dict(os.environ)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#!/bin/bash\n")
        f.write("# Generated from Windows environment variables\n\n")

        working_vars = ["PATH"]

        for name in working_vars:
            value = env_vars.get(name)
            if value is None:
                continue
            converted_value = convert_value(value)
            escaped_value = converted_value.replace('"', '\\"')
            f.write(f'export {name}="${name}:{escaped_value}"\n')

    print(f"File created: {output_file}")


if __name__ == "__main__":
    output_file = f"{os.getenv('HOME')}/.bashrc"
    generate_bashrc(output_file)
# python bin\env_to_bashrc.py
# dos2unix %HOME%\.bashrc
