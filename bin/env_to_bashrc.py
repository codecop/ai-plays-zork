#!/usr/bin/env python


import os
import re


class EnvironmentToBashrc:
    """
    Converts Windows environment variable PATH to a bashrc file.
    """

    def __init__(self, env_vars, base_path):
        self._env_vars = env_vars
        self._base_path = base_path

    def normalize_path(self, path):
        return (
            path.replace("\\", "/")
            .replace("/Program Files/", "/Progra~1/")
            .replace("/Program Files (x86)/", "/Progra~2/")
            .replace(" ", "\\ ")
        )

    def convert_path(self, path):
        if re.match(r"^[A-Za-z]:", path):
            drive = path[0].lower()
            rest = self.normalize_path(path[2:])
            converted = self._base_path + drive + rest
        else:
            converted = self.normalize_path(path)
        return converted

    def convert_path_list(self, value):
        converted_paths = [self.convert_path(path) for path in value.split(";")]
        return ":".join(converted_paths)

    def is_path_variable(self, value):
        return ";" in value and ("\\" in value or ":" in value)

    def convert_value(self, value):
        if self.is_path_variable(value):
            return self.convert_path_list(value)
        return self.convert_path(value)

    def generate_bashrc(self, output_file):
        with open(output_file, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("# Generated from Windows environment variables\n\n")

            working_vars = ["PATH"]

            for name in working_vars:
                value = self._env_vars.get(name)
                if value is None:
                    continue
                converted_value = self.convert_value(value)
                escaped_value = converted_value.replace('"', '\\"')
                f.write("export " + name + '="$' + name + ":" + escaped_value + '"\n')


if __name__ == "__main__":
    target = os.getenv("HOME") + "/.bashrc"
    # Cygwin     -> "/cygdrive/"
    # Msys/MingW -> "/"
    converter = EnvironmentToBashrc(os.environ, "/cygdrive/")
    converter.generate_bashrc(target)
    print("Created: " + target + " from environment")
