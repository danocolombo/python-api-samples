```markdown
# Deploy Notes — Offline Packaging (macOS Apple Silicon)

## Goal

Package this project so it can be moved to an **isolated macOS Apple Silicon** machine (with **Python 3.12 available**) and set up **without downloading anything**.

We’ll use:

- `wheelhouse/` (offline dependency wheels)
- a **fresh** `.venv/` created on the isolated Mac
- (optional) `bootstrap.sh` to make setup consistent

This is more reliable than copying `.venv/` across machines.

---

## On your connected (internet) Mac — build the offline bundle

### 1) Clean up local outputs (optional, keeps the zip small)

You typically don’t want to ship generated API response files:

- delete `data_files/` contents (or the whole folder), **or**
- exclude it from the zip later

Keeping it is fine if you want sample outputs included.

---

### 2) Freeze your exact dependencies

Activate your current venv and freeze:
```
bash
cd apiSample
source .venv/bin/activate
python -m pip freeze > requirements.txt
```
This captures exact versions currently working for you.

---

### 3) Download all dependencies into a wheelhouse (offline cache)

Create a `wheelhouse/` folder and download wheels:
```
bash
python -m pip download -r requirements.txt -d wheelhouse
```
**Strongly recommended check (wheels only)** — catches “would require compiling” problems before you’re offline:
```
bash
python -m pip download --only-binary=:all: -r requirements.txt -d wheelhouse
```
If the wheels-only command fails, it means at least one dependency doesn’t have a wheel available for your Python/architecture.

---

### 4) (Recommended) Add a minimal bootstrap script

Create `bootstrap.sh` in the project root:
```
bash
cat > bootstrap.sh <<'SH'
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
SH

chmod +x bootstrap.sh
```
This avoids the “python vs python3” ambiguity and guarantees installs are offline.

---

### 5) Zip the bundle (excluding `.venv/`)

Do **not** include `.venv/` in the zip (you’ll recreate it on the isolated machine).

From the directory **above** `apiSample/`:
```
bash
cd ..
zip -r apiSample_offline_bundle.zip apiSample \
  -x "apiSample/.venv/*" \
  -x "apiSample/__pycache__/*" \
  -x "apiSample/.DS_Store" \
  -x "apiSample/data_files/*"
```
Adjust the excludes as you like (you can keep `data_files/` if you want).

Your bundle should contain at least:

- project source (`*.py`, configs, README, etc.)
- `requirements.txt`
- `wheelhouse/`
- `bootstrap.sh` (optional but handy)

---

## On the isolated Mac — install offline and run

### Option A: One-command setup (recommended if you included `bootstrap.sh`)
```
bash
unzip apiSample_offline_bundle.zip
cd apiSample
./bootstrap.sh
source .venv/bin/activate
python main.py
```
### Option B: Manual setup (no bootstrap script)
```
bash
unzip apiSample_offline_bundle.zip
cd apiSample

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install --no-index --find-links wheelhouse -r requirements.txt

python main.py
```
---

## Quick validation checklist (offline)

After install:
```
bash
./.venv/bin/python -c "import sys; print(sys.version)"
./.venv/bin/python -m pip list
```
If those work, you’re good.

---

## Notes

- Keep `config.yml` out of version control if it contains secrets. When packaging for a test machine, include a sanitized config (use placeholders) or use a separate secure transfer mechanism for secrets.
- This project’s dependencies are small (e.g., `requests`, `PyYAML`), so the wheelhouse approach should be smooth.
```
