class Grammar:
    def __init__(self):
        self.non_terminals = set()
        self.terminals = set()
        self.start_symbol = None
        self.productions = {}  # dict of {Non-terminal: list of productions}

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                if '->' not in line:
                    continue
                head, body = line.strip().split('->')
                head = head.strip()
                bodies = [b.strip().split() for b in body.strip().split('|')]

                if self.start_symbol is None:
                    self.start_symbol = head

                self.non_terminals.add(head)
                self.productions.setdefault(head, []).extend(bodies)

        # استخراج ترمینال‌ها از تولیدها
        for rhs_list in self.productions.values():
            for rhs in rhs_list:
                for symbol in rhs:
                    if symbol != 'ε' and symbol not in self.productions:
                        self.terminals.add(symbol)

    def display(self):
        print("Start Symbol:", self.start_symbol)
        print("Non-terminals:", self.non_terminals)
        print("Terminals:", self.terminals)
        print("Productions:")
        for head, bodies in self.productions.items():
            print(f"  {head} -> {' | '.join([' '.join(prod) for prod in bodies])}")
