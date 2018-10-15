from pathlib import Path
from shutil import copyfile

Path('my_package').mkdir(exist_ok=True)
copyfile('../miniver/miniver/_static_version.py',
         'my_package/_static_version.py')
copyfile('../miniver/miniver/_version.py',
         'my_package/_version.py')

README_filename = '../miniver/README.md'


def write_snippet_from_readme(outfile, start_marker, file_header=None):
    # Create the setup file
    with open(README_filename) as f:
        for line in f:
            if line.startswith(start_marker):
                break
        else:
            raise RuntimeError('Could not find start_marker: {}'
                               ''.format(start_marker))
        with open(outfile, 'w') as out:
            out.write(line)
            if file_header is not None:
                out.write(file_header)
            for line in f:
                if line.startswith('```'):
                    break
                out.write(line)


write_snippet_from_readme("setup.py",
                          "# Your project's setup.py",
                          "from setuptools import setup\n")
write_snippet_from_readme(".gitattributes",
                          "# Your project's .gitattributes")
write_snippet_from_readme("my_package/__init__.py",
                          "# Your package's __init__.py")
