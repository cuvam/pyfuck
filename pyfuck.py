import ast
import string

class Minifier(ast.NodeTransformer):
    def __init__(self):
        self.names = {}
        self.counter = 0
        self.builtins = set(dir(__builtins__)) | {
            'print', 'range', 'len', 'int', 'str', 'list', 'dict',
            'set', 'tuple', 'float', 'bool', 'type', 'isinstance',
            'getattr', 'setattr', 'hasattr', 'exec', 'eval', 'chr',
            'ord', 'bytes', 'enumerate', 'zip', 'map', 'filter',
            'sorted', 'reversed', 'min', 'max', 'sum', 'abs', 'any',
            'all', 'open', 'super', 'property', 'classmethod',
            'staticmethod', 'None', 'True', 'False',
            '__name__', '__init__', '__str__', '__repr__',
            '__enter__', '__exit__', '__iter__', '__next__',
            '__getitem__', '__setitem__', '__len__', '__call__',
            '__class__', '__doc__', '__mro__', '__subclasses__',
        }

    def _short_name(self, name):
        if name.startswith('__') and name.endswith('__'):
            return name
        if name in self.builtins:
            return name
        if name not in self.names:
            self.names[name] = self._gen_name()
        return self.names[name]

    def _gen_name(self):
        chars = string.ascii_lowercase
        n = self.counter
        self.counter += 1
        result = chars[n % 26]
        n //= 26
        while n:
            n -= 1
            result = chars[n % 26] + result
            n //= 26
        return result

    def visit_Name(self, node):
        node.id = self._short_name(node.id)
        return node

    def visit_FunctionDef(self, node):
        node.name = self._short_name(node.name)
        if (node.body and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, (ast.Constant, ast.Str))):
            node.body = node.body[1:] or [ast.Pass()]
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        node.name = self._short_name(node.name)
        if (node.body and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, (ast.Constant, ast.Str))):
            node.body = node.body[1:] or [ast.Pass()]
        self.generic_visit(node)
        return node

    def visit_arg(self, node):
        node.arg = self._short_name(node.arg)
        node.annotation = None
        return node

    def visit_Import(self, node):
        for alias in node.names:
            self.builtins.add(alias.asname or alias.name)
        return node

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.builtins.add(alias.asname or alias.name)
        return node

    def visit_Global(self, node):
        node.names = [self._short_name(n) for n in node.names]
        return node

    def visit_Nonlocal(self, node):
        node.names = [self._short_name(n) for n in node.names]
        return node

def minify(source):
    tree = ast.parse(source)
    if (tree.body and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, (ast.Constant,))):
        tree.body = tree.body[1:]
    tree = Minifier().visit(tree)
    ast.fix_missing_locations(tree)
    lines = ast.unparse(tree).split('\n')
    out = []
    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if (out and not stripped.startswith(('def ', 'class ', 'if ', 'elif ',
                'else:', 'for ', 'while ', 'try:', 'except', 'finally:',
                'with ', 'return ', 'yield ', '@'))
                and not out[-1].rstrip().endswith(':')
                and len(out[-1]) - len(out[-1].lstrip()) == indent
                and len(out[-1]) + len(stripped) < 120):
            out[-1] = out[-1] + ';' + stripped
        else:
            out.append(line)
    return '\n'.join(out)

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

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <file.py>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        content = f.read()

    minified = minify(content)
    table = build_table(256)

    parts = []
    for ch in minified:
        parts.append(f"chr({table[ord(ch)]})")

    print("exec(" + "+".join(parts) + ")")