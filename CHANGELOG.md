# Changelog
All notable changes to miniver will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]
### Added
- Add a 'ver' command that prints the detected version

## [0.7.0] - 2020-08-15
### Added
- Allow distributions that place packages in a "src" directory
### Changed
- Replace tool "install-miniver" with a tool "miniver" with a command "install"
### Fixed
- Use "build_py" from setuptools, rather than distutils, which prevents a warning
  being displayed when using more recent setuptools versions

## [0.6.0] - 2019-02-17
### Fixed
- Typos in generated files (comments only)
- Dedented template code produced by 'install-miniver' to make it copy-pasteable.
