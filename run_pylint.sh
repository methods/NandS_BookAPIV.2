#!/bin/bash

# Activate virtual environment (adjust path if needed)
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
else
  echo "Warning: Virtual environment not found at venv/bin/activate"
fi



# Files to run pylint on
FILES="app.py test_app.py"
# Run pylint on the specified files
pylint $FILES
# Check the exit code to determine if Pylint passed or failed
if [ $? -eq 0 ]; then
    echo "Pylint passed successfully on all files."
else
    echo "Pylint found issues. Please fix them."
    exit 1
fi