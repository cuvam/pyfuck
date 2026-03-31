#!/bin/bash

# 1. Run pyfuck.py on itself
python3 pyfuck.py pyfuck.py > bs_pyfuck.py

# 2. Verify it works with hello world
python3 bs_pyfuck.py helloworld.py | python3 