which python
which python3

# 2. Choose the Python installation you want to keep
# For this example, let's assume it's the Python 3.12 installation

# 3. Create a list of essential pip packages
ESSENTIAL_PACKAGES="pip setuptools wheel packaging six"

# 4. Uninstall packages from pip3 (Python 3.12)
/Library/Frameworks/Python.framework/Versions/3.12/bin/pip3 freeze | grep -v "^-e" | cut -d "=" -f 1 | while read package; do
  if ! echo $ESSENTIAL_PACKAGES | grep -q $package; then
    /Library/Frameworks/Python.framework/Versions/3.12/bin/pip3 uninstall -y $package
  fi
done

# 5. Uninstall packages from pip (also Python 3.12 in this case)
/Library/Frameworks/Python.framework/Versions/3.12/bin/pip freeze | grep -v "^-e" | cut -d "=" -f 1 | while read package; do
  if ! echo $ESSENTIAL_PACKAGES | grep -q $package; then
    /Library/Frameworks/Python.framework/Versions/3.12/bin/pip uninstall -y $package
  fi
done

# 6. Upgrade pip to the latest version
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m pip install --upgrade pip

# 7. Verify the cleanup
/Library/Frameworks/Python.framework/Versions/3.12/bin/pip list
/Library/Frameworks/Python.framework/Versions/3.12/bin/pip3 list