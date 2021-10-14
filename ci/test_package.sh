set -e

distr=$1
pkg=$2

function test_version() {
    echo "Testing: $pkg.__version__$1"
    python -c "import $pkg; assert $pkg.__version__$1"
}

# "./" to ensure we don't pull from PyPI
pip install -e ./$distr

test_version "== 'unknown'"

pushd $distr
git add .
git commit -m "First commit"
git tag -a 0.0.0 -m "0.0.0"
echo "Tagged 0.0.0"
popd

test_version "== '0.0.0'"

pushd $distr
echo "# Extra comment" >> setup.py
echo "Modified working directory"
popd

test_version ".startswith('0.0.0')"
test_version ".endswith('dirty')"

pushd $distr
git commit -a -m "new comment"
echo "Committed changes"
popd

test_version ".startswith('0.0.0.dev1')"

pushd $distr
git tag -a 0.0.1 -m "0.0.1"
echo "Tagged 0.0.1"
popd

test_version "== '0.0.1'"

# Now test against "real" (non-editable) installations
pip uninstall -y $distr

pushd $distr
git commit --allow-empty -m 'next commit'
git tag -a 0.0.2 -m "0.0.2"
echo "Tagged 0.0.2"
popd

# First a source distribution

echo "Testing setup.py sdist"
pushd $distr
python setup.py sdist
pip install dist/*.tar.gz
popd

test_version "== '0.0.2'"

pip uninstall -y $distr

pushd $distr
git commit --allow-empty -m 'final commit'
git tag -a 0.0.3 -m "0.0.3"
echo "Tagged 0.0.3"
popd

# Then a wheel distribution

echo "Testing setup.py bdist_wheel"
pushd $distr
python setup.py bdist_wheel
pip install dist/*.whl
popd

test_version "== '0.0.3'"
