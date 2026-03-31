How it works:

1. Minify the source code
2. Extract ASCII code values from each character in minified source
3. Using the fact that `[]==[]` = 1 in Python, construct an equation using just 1's and `+`/`*`, then replace 1 with `[]==[]`, for each character
4. Wrap each obfuscated ASCII code in a `chr()` call, using `+` to concatenate them all together
5. Wrap entire obfuscated ASCII string in `exec()`

The result is a valid Python statement that has the same output as the original source code, and only uses the characters `+*()[]cehrx`.

Can be ran on itself to create a PyFuck-written Python to PyFuck transpiler, test with `bootstrap.sh`.
