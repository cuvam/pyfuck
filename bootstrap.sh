#!/bin/bash

# 1. Run pyfuck.py on itself
python3 pyfuck.py pyfuck.py > bs_pyfuck.py

# 2. Verify it works with hello world
python3 bs_pyfuck.py examples/helloworld.py | python3 

# 3. Verify bootstrap doesn't contain characters other than `+*=()[]cehrx`
match=$(grep -o -b -m 1 -E '[^][+*=()cehrx]' bs_pyfuck.py)
if [ -n "$match" ]; then
    offset="${match%%:*}"
    char="${match##*:}"
    echo "Disallowed character '$char' found at byte $offset"
else
    echo "No other characters in output"
fi