import setuptools
import subprocess


class GitSubmodulesUpdateCommand(setuptools.Command):
    description = "init and update git submodules"

    def run(self):
        subprocess.call(["git", "submodule", "update", "--init"])


class TheBuildCommand(setuptools.Command):
    description = "update submodules, then build as usual"

    def run(self):
        self._run_command('submodulesupdate')
        setuptools.command.build_py.build_py.run(self)


setuptools.setup(

    name = "mionixctl",
    version = "0.1",
#    package_dir={"": "mionix"},
#    packages = find_packages(),
    packages = ['mionix', 'mionix/python_hidraw/hidraw'],

    entry_points = {
        'console_scripts': [
            'mionixctl = mionix.mionixctl:main'
        ]
    },

    # metadata for upload to PyPI
    author = "Dimitris Tsitsipis",
    author_email = "mitsarionas@gmail.com",
    description = "A tool to configure the Mionix Avior 7000 Mouse",

    license = "GPL2",
    keywords = "mionix avior mouse",
    url = "https://github.com/dneto/senseictl",

    install_requires=[
        'ioctl-opt>=1.2',
        'pyudev>=0.16',
        'pyyaml>=3.10'
    ],
    cmdclass={
        "submodulesupdate": GitSubmodulesUpdateCommand,
        "build_py": TheBuildCommand
    }

)
