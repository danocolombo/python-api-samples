#!/usr/bin/env bash
set -euo pipefail

# Pick an available Python launcher
PYBIN=""
if command -v python3 >/dev/null 2>&1; then
  PYBIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYBIN="python"
else
  echo "ERROR: Neither python3 nor python found on PATH."
  exit 1
fi

# Require Python 3.12+
$PYBIN -c 'import sys; assert sys.version_info >= (3,12), sys.version' \
  || { echo "ERROR: Need Python 3.12+."; exit 1; }

# Create a fresh venv in the project folder
$PYBIN -m venv .venv

# Install dependencies strictly from local wheelhouse (offline)
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install --no-index --find-links wheelhouse -r requirements.txt

echo "Done."
echo "Activate: source .venv/bin/activate"
echo "Run:      python main.py"