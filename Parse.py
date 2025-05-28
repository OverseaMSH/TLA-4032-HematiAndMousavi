TERMINALS = {'PLUS', 'MINUS', 'STAR', 'DIV', 'POW', 'LEFT_PAR', 'RIGHT_PAR',
             'IDENTIFIER', 'LITERAL', 'EQ', 'EQEQ', 'LT', 'GT', 'COMMA', 'EOF'}


def parse(tokens, ll1, start_symbol):
    stack = ['EOF', start_symbol]
    i = 0
    while stack:
        top = stack.pop()
        current = tokens[i][0]
        if top == 'EOF' and current == 'EOF':
            print("Parsing operation was successful")
            return True
        if top in TERMINALS:
            if top == current:
                i += 1
            else:
                print(f"Error: expected {top} but found {current}")
                return False
        else:
            rule = ll1.get(top, {}).get(current)
            if rule is None:
                print(f"Error: no rule for {top} with lookahead {current}")
                return False
            for s in reversed(rule):
                if s != 'ε':
                    stack.append(s)
    return False
