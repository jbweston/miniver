# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 5):
    print("Miniver needs at least Python 3.5.")
    sys.exit(1)


# Loads version.py module without importing the whole package.
def get_version_and_cmdclass(pkg_path):
    import os
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("version", os.path.join(pkg_path, "_version.py"))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.get_cmdclass(pkg_path)


version, cmdclass = get_version_and_cmdclass("miniver")

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name="miniver",
    description="minimal versioning tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    url="https://github.com/jbweston/miniver",
    author="Joseph Weston and Christoph Groth",
    author_email="joseph@weston.cloud",
    license="CC0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Topic :: Software Development :: Version Control :: Git",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=find_packages("."),
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": [
            "miniver=miniver.app:main",
        ]
    },
)
