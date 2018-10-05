import setuptools


setuptools.setup(

    name = "mionixctl",
    version = "0.1",
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

)
