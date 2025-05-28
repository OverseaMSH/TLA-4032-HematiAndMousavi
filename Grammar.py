"""
GRAMMAR:

E  -> T E'
E' -> PLUS T E' | MINUS T E' | ε
T  -> F T'
T' -> STAR F T' | DIV F T' | ε
F  -> P F'
F' -> POW P F' | ε
P  -> LEFT_PAR E RIGHT_PAR | IDENTIFIER | LITERAL
"""

GRAMMAR = {
    'E': [['T', "E'"]],
    "E'": [['PLUS', 'T', "E'"], ['MINUS', 'T', "E'"], ['ε']],
    'T': [['F', "T'"]],
    "T'": [['STAR', 'F', "T'"], ['DIV', 'F', "T'"], ['ε']],
    'F': [['P', "F'"]],
    "F'": [['POW', 'P', "F'"], ['ε']],
    'P': [['LEFT_PAR', 'E', 'RIGHT_PAR'], ['IDENTIFIER'], ['LITERAL']],
}

FIRST = {
    'E': {'LEFT_PAR', 'IDENTIFIER', 'LITERAL'},
    "E'": {'PLUS', 'MINUS', 'ε'},
    'T': {'LEFT_PAR', 'IDENTIFIER', 'LITERAL'},
    "T'": {'STAR', 'DIV', 'ε'},
    'F': {'LEFT_PAR', 'IDENTIFIER', 'LITERAL'},
    "F'": {'POW', 'ε'},
    'P': {'LEFT_PAR', 'IDENTIFIER', 'LITERAL'},
}

FOLLOW = {
    'E': {'RIGHT_PAR', 'EOF'},
    "E'": {'RIGHT_PAR', 'EOF'},
    'T': {'PLUS', 'MINUS', 'RIGHT_PAR', 'EOF'},
    "T'": {'PLUS', 'MINUS', 'RIGHT_PAR', 'EOF'},
    'F': {'STAR', 'DIV', 'PLUS', 'MINUS', 'RIGHT_PAR', 'EOF'},
    "F'": {'STAR', 'DIV', 'PLUS', 'MINUS', 'RIGHT_PAR', 'EOF'},
    'P': {'POW', 'STAR', 'DIV', 'PLUS', 'MINUS', 'RIGHT_PAR', 'EOF'},
}


def build_ll1_table(grammar, first, follow):
    table = {}
    for nt in grammar:
        for prod in grammar[nt]:
            first_set = set()
            if prod[0] == 'ε':
                first_set = {'ε'}
            else:
                for symbol in prod:
                    if symbol in first:
                        first_set |= (first[symbol] - {'ε'})
                        if 'ε' not in first[symbol]:
                            break
                    else:
                        first_set.add(symbol)
                        break
                else:
                    first_set.add('ε')
            for terminal in first_set - {'ε'}:
                table.setdefault(nt, {})[terminal] = prod
            if 'ε' in first_set:
                for terminal in follow[nt]:
                    table.setdefault(nt, {})[terminal] = prod
    return table
