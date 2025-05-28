from Compile import compile
from Parse import parse
from Grammar import GRAMMAR, FIRST, FOLLOW, build_ll1_table

inp = "f(x)"
tokens = compile(inp)

if not tokens:
    print("Compilation failed due to invalid tokens. Parsing aborted.")
else:
    t = build_ll1_table(GRAMMAR, FIRST, FOLLOW)
    result = parse(tokens, t, 'E')
    print("Result:", result)
