# This file is part of 'miniver': https://github.com/jbweston/miniver

import sys
import os
import os.path
import argparse
import tempfile
import shutil
import textwrap
import glob
from zipfile import ZipFile
from importlib.util import find_spec, spec_from_file_location, module_from_spec
from urllib.request import urlretrieve

if sys.version_info < (3, 5):
    print("Miniver needs at least Python 3.5")
    sys.exit(1)

try:
    import miniver

    _miniver_version = miniver.__version__
    del miniver
    _miniver_is_installed = True
except ImportError:
    _miniver_version = "unknown"
    _miniver_is_installed = False

# When we fetch miniver from local files
_miniver_modules = ("_version",)


# When we fetch miniver from GitHub
_miniver_zip_url = "https://github.com/jbweston/miniver/archive/master.zip"
_zipfile_root = "miniver-master"  # tied to the fact that we fetch master.zip

# File templates
_setup_template = textwrap.dedent(
    '''
    from setuptools import setup

    def get_version_and_cmdclass(pkg_path):
        """Load version.py module without importing the whole package.

        Template code from miniver
        """
        import os
        from importlib.util import module_from_spec, spec_from_file_location

        spec = spec_from_file_location("version", os.path.join(pkg_path, "_version.py"))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.__version__, module.get_cmdclass(pkg_path)


    version, cmdclass = get_version_and_cmdclass(r"{package_dir}")


    setup(
        ...,
        version=version,
        cmdclass=cmdclass,
    )
'''
)

_static_version_template = textwrap.dedent(
    """\
    # -*- coding: utf-8 -*-
    # This file is part of 'miniver': https://github.com/jbweston/miniver
    #
    # This file will be overwritten by setup.py when a source or binary
    # distribution is made.  The magic value "__use_git__" is interpreted by
    # version.py.

    version = "__use_git__"

    # These values are only set if the distribution was created with 'git archive'
    refnames = "$Format:%D$"
    git_hash = "$Format:%h$"
"""
)

_init_template = "from ._version import __version__"
_gitattribute_template = "{package_dir}/_static_version.py export-subst"


def _line_in_file(to_find, filename):
    """Return True if the specified line exists in the named file."""
    assert "\n" not in to_find
    try:
        with open(filename) as f:
            for line in f:
                if to_find in line:
                    return True
            return False
    except FileNotFoundError:
        return False


def _write_line(content, filename):
    assert "\n" not in content
    if not _line_in_file(content, filename):
        with open(filename, "a") as f:
            f.write(content)


def _write_content(content, filename):
    with open(filename, "w") as f:
        f.write(content)


def _fail(msg):
    print(msg, file=sys.stderr)
    print("Miniver was not installed", file=sys.stderr)
    sys.exit(1)


def extract_miniver_from_github():
    filename, _ = urlretrieve(_miniver_zip_url)
    z = ZipFile(filename)
    tmpdir = tempfile.mkdtemp()
    input_paths = [
        "/".join((_zipfile_root, "miniver", module + ".py"))
        for module in _miniver_modules
    ]
    for p in input_paths:
        z.extract(p, path=tmpdir)
    return [os.path.join(tmpdir, *p.split()) for p in input_paths]


def extract_miniver_from_local():
    return [
        find_spec("." + module, package="miniver").origin for module in _miniver_modules
    ]


def get_parser():
    parser = argparse.ArgumentParser(description="Interact with miniver")
    parser.add_argument("-v", "--version", action="version", version=_miniver_version)
    # TODO: when we can depend on Python 3.7 make this "add_subparsers(required=True)"
    subparsers = parser.add_subparsers()
    # 'install' command
    install_parser = subparsers.add_parser(
        "install", help="Install miniver into the current Python package"
    )
    install_parser.add_argument(
        "package_directory", help="Directory to install 'miniver' into."
    )
    install_parser.set_defaults(dispatch=install)
    # 'ver' command
    ver_parser = subparsers.add_parser(
        "ver", help="Display generated version",
    )
    ver_parser.add_argument(
        "search_path",
        help="Path to begin search for version files",
        nargs="?",
        default=".",
    )
    ver_parser.set_defaults(dispatch=ver)
    return parser


def install(args):
    package_dir = args.package_directory
    if not os.path.isdir(package_dir):
        _fail("Directory '{}' does not exist".format(package_dir))
    if package_dir != os.path.relpath(package_dir):
        _fail("'{}' is not a relative directory".format(package_dir))

    # Get miniver files
    if _miniver_is_installed:
        miniver_paths = extract_miniver_from_local()
    else:
        miniver_paths = extract_miniver_from_github()
    output_paths = [
        os.path.join(package_dir, os.path.basename(path)) for path in miniver_paths
    ]

    for path in output_paths:
        if os.path.exists(path):
            _fail("'{}' already exists".format(path))

    # Write content to local package directory
    for path, output_path in zip(miniver_paths, output_paths):
        shutil.copy(path, output_path)
    _write_content(
        _static_version_template, os.path.join(package_dir, "_static_version.py")
    )
    _write_line(
        _gitattribute_template.format(package_dir=package_dir), ".gitattributes"
    )
    _write_line(
        _init_template.format(package_dir=package_dir),
        os.path.join(package_dir, "__init__.py"),
    )

    msg = "\n".join(
        textwrap.wrap(
            "Miniver is installed into '{package_dir}/'. "
            "You still have to copy the following snippet into your 'setup.py':"
        )
    )
    # Use stdout for setup template only, so it can be redirected to 'setup.py'
    print(msg.format(package_dir=package_dir), file=sys.stderr)
    print(_setup_template.format(package_dir=package_dir), file=sys.stdout)


def ver(args):
    search_path = os.path.realpath(args.search_path)
    try:
        version_location, = glob.glob(
            os.path.join(search_path, "**", "_version.py"),
            recursive=True,
        )
    except ValueError as err:
        if "not enough" in str(err):
            print(
                "'_version.py' not found in '{}'".format(search_path),
                file=sys.stderr,
            )
            sys.exit(1)
        elif "too many" in str(err):
            print(
                "More than 1 '_version.py' found in '{}'".format(search_path),
                file=sys.stderr,
            )
            sys.exit(1)
        else:
            raise
    version_spec = spec_from_file_location("version", version_location)
    version = module_from_spec(version_spec)
    version_spec.loader.exec_module(version)
    print(version.get_version())


def main():
    parser = get_parser()
    args = parser.parse_args()
    # TODO: remove this check when we can rely on Python 3.7 and
    #       can make subparsers required.
    if "dispatch" in args:
        args.dispatch(args)
    else:
        args = parser.parse_args(["ver"])
        args.dispatch(args)


# This is needed when using the script directly from GitHub, but not if
# miniver is installed.
if __name__ == "__main__":
    main()
