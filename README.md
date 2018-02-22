# Miniver
[![License: CC0-1.0][cc0_badge]][cc0]

**Like [versioneer][versioneer], but smaller**

Miniver is a **mini**mal **ver**sioning tool that serves the same purpose
as [Versioneer][versioneer], except that it is not designed to be
cross platform, and only works with Git.

#### Why would I use this?
If you are developing a Python package inside a Git repository and
want to get the version directly from Git tags, rather than hard-coding
version strings everywhere.

This is the same problem that Versioneer solves, but Miniver is less
than 200 lines of code, whereas Versioneer is over 2000. The tradeoff
is that Miniver only works with Git, and has not been tested across
different platforms and Python versions (yet).


[versioneer]: https://github.com/warner/python-versioneer
[cc0_badge]: https://licensebuttons.net/l/zero/1.0/88x31.png
[cc0]: http://creativecommons.org/publicdomain/zero/1.0/

## Usage
Copy the contents of the `miniver` directory (in this repository) into your
project's main package directory.

Then copy the following snippets into the appropriate files:

```python
# Your package's __init__.py
from . import version
__version__ = version.version
del version
```

```python
# Your project's setup.py

# Loads version.py module without importing the whole package.
def get_version_and_cmdclass(package_name):
    import os
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location('version',
                                   os.path.join(package_name, 'miniver.py'))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.version, module.cmdclass


version, cmdclass = get_version_and_cmdclass('my_package')

setup(
    name='my_package',
    version=version,
    cmdclass=cmdclass,
)
```

```
# Your project's .gitattributes
my_package/_static_version.py export-subst
```

replacing `'my_package'` in the above with the name of your package
(this should be the same as the name of the directory into
which you copied the contents of `miniver`).

That's it!

## License
Miniver is in the public domain under a CC0 license.
