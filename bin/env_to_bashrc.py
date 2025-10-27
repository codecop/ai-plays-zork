#!/usr/bin/env python

import os
import re


def normalize_slashes(path):
    return path.replace("\\", "/")


def convert_path(path):
    if re.match(r"^[A-Za-z]:", path):
        drive = path[0].lower()
        rest = normalize_slashes(path[2:])
        return f"/cygdrive/{drive}{rest}"

    return normalize_slashes(path)


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

        for name, value in sorted(env_vars.items()):
            converted_value = convert_value(value)
            escaped_value = converted_value.replace('"', '\\"')
            f.write(f'export {name}="{escaped_value}"\n')

    print(f"Bashrc file created: {output_file}")


if __name__ == "__main__":
    output_file = "bashrc"
    generate_bashrc(output_file)
