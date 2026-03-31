How it works:

1. Minify the source code
2. Extract ASCII code values from each character in minified source
3. Using the fact that, in Python, `[]==[]` = `True`, and performing arithmetic on `True` coerces it to `1`, construct an equation using just 1's and `+`/`*` for each ASCII code, then replace 1 with `[]==[]` for each resulting expression
4. Wrap each obfuscated ASCII code expression in a `chr()` call, using `+` to concatenate them all together into a string
5. Wrap entire obfuscated ASCII statement string in `exec()` to run the obfuscated statement

The result is a valid Python statement that has the same output as the original source code, and only uses the characters `+*=()[]cehrx`.

Can be ran on itself to create a PyFuck-written Python to PyFuck transpiler, test with `bootstrap.sh`.

I do realize that you could get it down to 10 characters by not replacing every `1` with `[]==[]`, removing `[]=`, and including `1` in the allowed character set. But that would be no fun.

Inspired by JSFuck.
