#!/bin/bash

# 1. Run pyfuck.py on itself
python3 pyfuck.py pyfuck.py > bs_pyfuck.py

# 2. Verify it works with hello world
python3 bs_pyfuck.py examples/src/helloworld.py | python3 

# 3. Verify bootstrap doesn't contain characters other than allowed set
# Allowed: [ ] ( ) + * = % ' _ c e x
match=$(grep -o -b -m 1 -E "[^][+*=()%cex']" bs_pyfuck.py)
if [ -n "$match" ]; then
    offset="${match%%:*}"
    char="${match##*:}"
    echo "Disallowed character '$char' found at byte $offset"
else
    echo "No other characters in output"
fi