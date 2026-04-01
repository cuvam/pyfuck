#!/bin/bash
cd "$(dirname "$0")"

# TRANSPILE EXAMPLE PYTHON FILES TO PYFUCK
for src in src/*.py; do
    base=$(basename "$src" .py)
    echo "Compiling $src -> ${base}_pf.py"
    python3 ../pyfuck.py "$src" > "fucked_src/${base}_pf.py"
done

# RUN PYFUCK FILES
for f in fucked_src/*.py; do
    echo "=== $(basename "$f") ==="
    python3 "$f"
done