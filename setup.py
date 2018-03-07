# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 5):
    print('Miniver needs at least Python 3.5.')
    sys.exit(1)

# Loads version.py module without importing the whole package.
def get_version_and_cmdclass(package_name):
    import os
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location('version',
                                   os.path.join(package_name, '_version.py'))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.cmdclass


version, cmdclass = get_version_and_cmdclass('miniver')


setup(
    name='miniver',
    description='minimal versioning tool',
    version=version,
    url='https://github.com/jbweston/miniver',
    author='Joseph Weston and Christoph Groth',
    author_email='joseph@weston.cloud',
    license='CC0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Topic :: Software Development :: Version Control :: Git',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages('.'),
    cmdclass=cmdclass,
    scripts=['install-miniver']
)
