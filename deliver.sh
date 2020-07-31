#!/bin/bash

source venv/bin/activate

# configuration management
git rebase
git status

# version management
VERSION=`grep "version =" pyproject.toml | sed -e 's/.*= "//' -e 's/"//'`
VERSION="v${VERSION}"
echo "Version to be delivered: ${VERSION}"
echo -n "Is it OK? (y/n) [y]: "
read BOOL
if [ "$BOOL" == "n" ]
then
    exit 1
fi
echo ""

# changelog management
grep -A 30 Changelog README.md 
echo -n "Do you want to add something in README.md? (y/n) [n]: "
read BOOL
if [ "$BOOL" == "y" ]
then
    exit 1
fi
echo ""

# clean
rm -rf build/ dist/ .eggs/
find . -name '*.egg-info' -exec rm -fr {} +
find . -name '*.egg' -exec rm -fr {} +
find . -name '*.pyc' -exec rm -f {} +
find . -name '*.pyo' -exec rm -f {} +
find . -name '*~' -exec rm -f {} +
find . -name '__pycache__' -exec rm -fr {} +
rm -fr .tox/
rm -f .coverage
rm -fr htmlcov/
rm -fr .pytest_cache

# tests
tox
echo -n "Is it OK? (y/n) [y]: "
read BOOL
if [ "$BOOL" == "n" ]
then
    exit 1
fi
echo ""

# git tag + push
git tag -a $VERSION -m "Version ${VERSION}"
until git push
do
  echo "Try again"
done
until git push --tags
do
  echo "Try again"
done

# package creation
poetry build
until poetry publish
do
  echo "Try again"
done

echo "Done"
