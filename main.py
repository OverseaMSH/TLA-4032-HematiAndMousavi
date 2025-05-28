from Compile import compile
code = """x = sin(2.5) + y^2 - 3 /{cccc z\
    
    
"""
tokens = compile(code)
for tok in tokens:
    print(tok)