#!/bin/bash
cd "$(dirname "$0")"

for src in src/*.py; do
    base=$(basename "$src" .py)
    echo "Compiling $src -> ${base}_pf.py"
    python3 ../pyfuck.py "$src" > "${base}_pf.py"
done