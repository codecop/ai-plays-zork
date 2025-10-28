import os
import tempfile
import unittest
from env_to_bashrc import EnvironmentToBashrc


class TestEnvironmentToBashrc(unittest.TestCase):

    def test_generate_bashrc_cygwin(self):
        env_vars = {
            "PATH": "C:\\Program Files\\Git\\bin;C:\\Windows\\System32;D:\\tools"
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".bashrc", delete=False) as f:
            output_file = f.name

        try:
            converter = EnvironmentToBashrc(env_vars, "/cygdrive/")
            converter.generate_bashrc(output_file)

            with open(output_file, "r") as f:
                content = f.read()

            self.assertIn("#!/bin/bash", content)
            self.assertIn(
                'export PATH="$PATH:/cygdrive/c/Progra~1/Git/bin:/cygdrive/c/Windows/System32:/cygdrive/d/tools"',
                content,
            )
        finally:
            os.remove(output_file)

    def test_normalize_path(self):
        converter = EnvironmentToBashrc({}, "/cygdrive/")

        self.assertEqual(
            converter.normalize_path("C:\\Program Files\\test"), "C:/Progra~1/test"
        )
        self.assertEqual(
            converter.normalize_path("C:\\Program Files (x86)\\app"), "C:/Progra~2/app"
        )
        self.assertEqual(
            converter.normalize_path("C:\\my folder\\file"), "C:/my\\ folder/file"
        )


if __name__ == "__main__":
    unittest.main()
