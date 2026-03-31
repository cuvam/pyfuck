How it works:
 
1. Minify the source code
2. Extract ASCII code values from each character in minified source
3. Using the fact that, in Python, `[]==[]` = `True`, and performing arithmetic on `True` coerces it to `1`, construct an expression using just 1's and `+`/`*` for each ASCII code
4. Replace `1` with `[]==[]` in each resulting ASCII code expression
5. Use Python's `'%c'%` string formatting to convert each obfuscated integer expression into its character, using `+` to concatenate them all together into a string
6. Assign the string to `x` in chunks (to avoid hitting Python's recursion limit during compilation), then `exec(x)` to run it
 
The result is a valid Python program that has the same output as the original source code, and only uses 12 distinct characters: `%'()*+=[]cex`.
  
Can be ran on itself to create a PyFuck-written Python to PyFuck transpiler, test with `bootstrap.sh`.
 
Inspired by JSFuck.