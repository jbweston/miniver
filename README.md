# Miniver
[![license: CC0-1.0](https://img.shields.io/pypi/l/miniver.svg)][cc0]
[![PyPI version](https://img.shields.io/pypi/v/miniver.svg)][pypi]
[![Travis build](https://travis-ci.org/jbweston/miniver.svg)][travis]
[![Appveyor build](https://ci.appveyor.com/api/projects/status/v9q0hmjfm9qxdsi4?svg=true)][appveyor]

**Like [versioneer][versioneer], but smaller**

Miniver is a **mini**mal **ver**sioning tool that serves the same purpose
as [Versioneer][versioneer], except that it only works with Git and
multiplatform support is still experimental.

#### Why would I use this?
If you are developing a Python package inside a Git repository and
want to get the version directly from Git tags, rather than hard-coding
version strings everywhere.

This is the same problem that Versioneer solves, but Miniver is less
than 200 lines of code, whereas Versioneer is over 2000. The tradeoff
is that Miniver only works with Git and Python 3.5 (or above), and has only been
tested on Debian Linux and Mac OSX (automated with Travis) and for Windows
on Appveyor.

Support for Python 2 is not a goal, as Python 2 is fast approaching its
end of life (2020), and we want to encourage people to use Python 3!
That being said, Christian Marquardt has a [fork that also
works with Python 2](https://github.com/cmarquardt/miniver2)

[versioneer]: https://github.com/warner/python-versioneer
[cc0]: http://creativecommons.org/publicdomain/zero/1.0/
[pypi]: https://pypi.org/project/miniver/
[travis]: https://travis-ci.org/jbweston/miniver
[appveyor]: https://ci.appveyor.com/project/jbweston/miniver

## Usage
The simplest way to use Miniver is to run the following in your project root:
```
curl https://raw.githubusercontent.com/jbweston/miniver/master/install-miniver | python - <your_package_directory>
```
This will grab the latest files from GitHub and set up Miniver for your project.

### I get an `unknown` version!
The version is reported as `unknown` (plus the current git hash) when there are no valid tags
in the git history. You should create an [*annotated tag*](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
so that Miniver reports a reasonable version.

If your project uses *unannotated tags* for versioning (though this is not the
[recommended way](https://stackoverflow.com/questions/11514075/what-is-the-difference-between-an-annotated-and-unannotated-tag))
then you'll need to run the following in order to modify Miniver's behaviour:
```
curl https://raw.githubusercontent.com/jbweston/miniver/master/unannotated-tags.patch | patch <your_package_directory>/_version.py
```

### I don't want to type that URL every time I use this
You can `pip install miniver`, which will give you the `install-miniver` script.
Then you can simply run the following from your project root to use Miniver:
```
install-miniver <your_package_directory>
```

### Can I use this without executing random code from the internet?
Sure! Copy `miniver/_version.py` and `miniver/_static_version.py` from this
repository into your package directory, then copy the following snippets into
the appropriate files:

```python
# Your package's __init__.py
from ._version import __version__
del _version
```

```python
# Your project's setup.py

# Loads _version.py module without importing the whole package.
def get_version_and_cmdclass(package_name):
    import os
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location('version',
                                   os.path.join(package_name, '_version.py'))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.cmdclass


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
