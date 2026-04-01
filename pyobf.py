"""
PyFuck transpiler that can be used from the REPL (without minification).
Usage: `from pyobf import *`, then:
* `obf_source(source)` to obfuscate Python source code
* `exec_obf(obf_source)` to execute the obfuscated string
Example:
```
>>> osrc = obf_source('print("Hello, world!")')
>>> len(osrc)
3211
>>> exec_obf(osrc)
Hello, world!
```
"""

def build_table(limit=256):
    ONE = "[]==[]"
    cost = [0, 1] + [float('inf')] * (limit - 1)
    expr = ["", ONE] + [""] * (limit - 1)

    for i in range(2, limit + 1):
        for a in range(2, int(i**0.5) + 1):
            if i % a == 0:
                b = i // a
                c = cost[a] + cost[b]
                if c < cost[i]:
                    cost[i] = c
                    expr[i] = f"({expr[a]})*({expr[b]})"
        for a in range(1, i // 2 + 1):
            b = i - a
            c = cost[a] + cost[b]
            if c < cost[i]:
                cost[i] = c
                expr[i] = f"({expr[a]})+({expr[b]})"

    return expr

_OBF_NUM_TABLE = build_table()

def exec_obf(obf_source):
    exec(eval(obf_source), {})

def obf_source(source):
    chs = []
    for ch in source:
        chs.append(ord(ch))
    enc = ''
    for cc in map(lambda x: f'"%c"%({_OBF_NUM_TABLE[x]})', chs):
        enc += cc + '+'
    enc = enc[:-1]
    return enc
