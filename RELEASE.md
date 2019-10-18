# Making a miniver release
These instructions can also be used as a starting point for packages that use miniver.

## Preflight checks

1. Verify that all issues/pull requests pertinent for this release are closed/merged
2. Verify that all changes are recorded in the changelog
3. Verify that any attribution files (e.g AUTHORS) are up to date
4. Verify that copyright notices are up to date
5. Verify that the builds are passing on `master`

## Prepare the release

1. Restore the git repository to a pristine state: `git checkout master && git reset --hard HEAD && git clean -xd -f`
2. Create a *signed*, *annotated* release tag: `git tag -as vX.Y.Z -m 'version X.Y.Z'`
3. Create source and binary distributions: `python setup.py sdist bdist_wheel`
4. Create an empty commit to start development towards the next release: `git commit --allow-empty -m 'start development towards A.B.C'`
5. Create a *signed*, *annotated* pre-release tag: `git tag -as vA.B.C-dev -m 'work towards A.B.C'`

## Publish the release
1. Push the new version and development tags: `git push upstream vX.Y.Z vA.B.C-dev`
2. Upload the distributions to PyPI: `twine upload dist/*`
