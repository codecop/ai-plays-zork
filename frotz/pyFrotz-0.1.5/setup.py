from setuptools import setup
from setuptools.command.install import install
import os
import subprocess


def compile_and_install_software():
    """Use the subprocess module to compile/install the C software."""
    dest_path = os.path.expanduser('~/.pyfrotz/')
    if os.path.exists(dest_path + 'dfrotz'):
        return # binary exists no need to build it
    elif not os.path.exists(dest_path):
        os.mkdir(dest_path)


class CustomInstall(install):
    """Custom handler for the 'install' command."""
    def run(self):
        compile_and_install_software()
        super().run()


setup(
    name='pyFrotz',
    version='0.1.5',
    packages=['pyfrotz'],
    url='https://github.com/OpenJarbas/pyFrotz',
    license='Apache2.0',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='minimal wrapper around frotz',
    cmdclass={'install': CustomInstall}
)
