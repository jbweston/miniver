import argparse
from contextlib import contextmanager
from functools import partial
import os.path
from os import chdir, makedirs
from shutil import rmtree
from subprocess import run, PIPE, CalledProcessError
from sys import exit, stderr
from textwrap import indent


@contextmanager
def log(msg, where=stderr):
    pp = partial(print, file=where)
    pp("{}...".format(msg), end="")
    try:
        yield
    except KeyboardInterrupt:
        pp("INTERRUPTED")
        exit(2)
    except CalledProcessError as e:
        pp("FAILED")
        pp("Subprocess '{}' failed with exit code {}".format(e.cmd, e.returncode))
        if e.stdout:
            pp("---- stdout ----")
            pp(e.stdout.decode())
            pp("----------------")
        if e.stderr:
            pp("---- stderr ----")
            pp(e.stderr.decode())
            pp("----------------")
        exit(e.returncode)
    except Exception as e:
        print("FAILED", file=where)
        print(str(e), file=where)
        exit(1)
    else:
        print("OK", file=where)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("distribution", help="Distribution package name")
    parser.add_argument("package", help="Dotted package name")
    parser.add_argument("--src-layout", action="store_true")
    args = parser.parse_args()

    distr, pkg, src_pkg = (getattr(args, x) for x in ("distribution", "package", "src_layout"))

    path = os.path.join("src" if src_pkg else "", pkg.replace(".", os.path.sep))

    with log("Ensuring '{}' is removed".format(distr)):
        rmtree(args.distribution, ignore_errors=True)

    with log("Initializing git repository in '{}'".format(distr)):
        run("git init {}".format(distr), check=True, stdout=PIPE, stderr=PIPE)
        chdir(distr)
        makedirs(path)

    with log("Installing miniver in '{}'".format(os.path.join(distr, path))):
        r = run(
            "miniver install {}".format(path),
            check=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        setup_template = r.stdout.decode("utf8")

    with log("Writing gitignore"):
        with open(".gitignore", "w") as f:
            f.write("\n".join([
                "dist",
                "build",
                "__pycache__",
                "*.egg-info",
            ]))

    with log("Writing setup.py"):
        lines = [
            "name='{}',".format(distr),
            "packages=['{}'],".format(pkg),
        ]
        if src_pkg:
            lines.append("package_dir={'': 'src'},")
        replacement = indent("\n".join(lines), "    ")

        with open("setup.py", "w") as f:
            # This is tightly coupled to the setup.py template: there is a
            # call to 'setup()' with an ellipsis on a single line.
            f.write(setup_template.replace("    ...,", replacement))


if __name__ == "__main__":
    main()
