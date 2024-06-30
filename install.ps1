try { python -m build }
catch { throw "Could not build the package. Make sure you have 'build' installed in the current environment using 'pip install build'." }

try { $WheelFile = gci dist\*.whl | select -last 1; pip install -U $WheelFile }
catch { throw "Could not install cline." }
