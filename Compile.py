import re
GRAMMER_REGEX = [
    ('EQEQ', r'=='),
    ('EQ', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('STAR', r'\*'),
    ('DIV', r'/'),
    ('POW', r'\^'),
    ('LT', r'<'),
    ('GT', r'>'),
    ('LEFT_PAR', r'\('),
    ('RIGHT_PAR', r'\)'),
    ('COMMA', r','),
    ('LITERAL', r'\d+(\.\d+)?'),                  # float or decimal
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),    # varibale
    ('SKIP', r'[ \t\n]+'),                        # space or tabs or new lines
    ('MISMATCH', r'.'),                           # others
]


def compile(g):
    grammers = []
    grammersRegex = '|'.join(
        f'(?P<{name}>{pattern})' for name, pattern in GRAMMER_REGEX)
    for i in re.finditer(grammersRegex, g):
        model = i.lastgroup
        value = i.group()
        if model == 'SKIP':
            continue
        elif model == 'MISMATCH':
            print(f'Error in compiling -> MISMATCH: "{value}"')
            return []
        grammers.append((model, value))
    grammers.append(('EOF', '$'))
    return grammers
