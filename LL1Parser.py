from Grammar import Grammar
from DPDA import DPDA

class LL1Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.first = {nt: set() for nt in self.grammar.non_terminals}
        self.follow = {nt: set() for nt in self.grammar.non_terminals}
        self.parse_table = {}

    def compute_first(self):
        """
        محاسبهٔ مجموعهٔ FIRST برای هر غیرپایانه.
        """
        # ۱) ابتدا همهٔ FIRSTها را خالی می‌کنیم و nullable را False می‌گیریم
        nullable = {nt: False for nt in self.grammar.non_terminals}
        self.first = {nt: set() for nt in self.grammar.non_terminals}

        changed = True
        while changed:
            changed = False
            for head, bodies in self.grammar.productions.items():
                for body in bodies:
                    # اگر تولید A -> ε باشد:
                    if body == ['ε']:
                        # علامت ε را به FIRST(head) اضافه کن
                        if 'ε' not in self.first[head]:
                            self.first[head].add('ε')
                            changed = True
                        # و head را nullable بنما
                        if not nullable[head]:
                            nullable[head] = True
                            changed = True
                        continue

                    # در غیر این صورت، قدم‌به‌قدم از چپ به راست عناصر body را بررسی می‌کنیم
                    prefix_nullable = True
                    for symbol in body:
                        # --- اگر سمبل یک ترمینال باشد ---
                        if symbol in self.grammar.terminals:
                            if symbol not in self.first[head]:
                                self.first[head].add(symbol)
                                changed = True
                            prefix_nullable = False
                            break

                        # --- اگر سمبل یک غیرپایانه باشد ---
                        if symbol in self.grammar.non_terminals:
                            # همهٔ FIRST(symbol) بجز ε را به FIRST(head) اضافه کن
                            for t in self.first[symbol]:
                                if t != 'ε' and t not in self.first[head]:
                                    self.first[head].add(t)
                                    changed = True
                            # اگر ε در FIRST(symbol) باشد، prefix_nullable همچنان True
                            if 'ε' in self.first[symbol]:
                                prefix_nullable = True
                            else:
                                prefix_nullable = False
                            if not prefix_nullable:
                                break
                            continue

                        # --- در غیر این دو حالت (احتمال قریب به یقین ندارد) ---
                        if symbol not in self.first[head]:
                            self.first[head].add(symbol)
                            changed = True
                        prefix_nullable = False
                        break

                    # اگر همهٔ سمبل‌های body nullable بودند (یا body تهی بود و ما از ابتدا ε داشتیم)
                    if prefix_nullable:
                        if 'ε' not in self.first[head]:
                            self.first[head].add('ε')
                            changed = True

        return self.first

    def compute_follow(self):
        """
        محاسبهٔ مجموعهٔ FOLLOW برای هر غیرپایانه.
        """
        # ابتدا همهٔ FOLLOWها را خالی می‌کنیم
        self.follow = {nt: set() for nt in self.grammar.non_terminals}
        # علامت $ را به FOLLOW(start_symbol) اضافه کن
        self.follow[self.grammar.start_symbol].add('$')

        changed = True
        while changed:
            changed = False
            for head, bodies in self.grammar.productions.items():
                for body in bodies:
                    trailer = set(self.follow[head])  # شروعِ تابع با FOLLOW(A)
                    # از انتهای بدنه به جلو برو
                    for symbol in reversed(body):
                        if symbol in self.grammar.non_terminals:
                            before = set(self.follow[symbol])
                            self.follow[symbol].update(trailer)
                            if self.follow[symbol] != before:
                                changed = True
                            # اگر ε ∈ FIRST(symbol)، تریلر = تریلر ∪ (FIRST(symbol) - {ε})
                            if 'ε' in self.first[symbol]:
                                trailer = trailer.union(self.first[symbol] - {'ε'})
                            else:
                                trailer = set(self.first[symbol] - {'ε'})
                        elif symbol in self.grammar.terminals:
                            trailer = {symbol}
                        else:
                            trailer = set()

        return self.follow

    def build_parse_table(self):
        """
        ساخت جدول LL(1) بر اساس مجموعه‌های FIRST و FOLLOW.
        """
        # ۱) محاسبهٔ FIRST و FOLLOW
        self.compute_first()
        self.compute_follow()

        # ===== چاپِ FOLLOW برای بررسی =====
        print("===== FOLLOW sets =====")
        for nt in sorted(self.grammar.non_terminals):
            print(f"FOLLOW({nt}) = {self.follow[nt]}")
        print("========================\n")

        # ۲) مقداردهی اولیه: همهٔ خانه‌ها None
        for nt in self.grammar.non_terminals:
            for t in self.grammar.terminals.union({'$'}):
                self.parse_table[(nt, t)] = None

        # ۳) پر کردن جدول برای هر تولید A -> α
        for head, bodies in self.grammar.productions.items():
            for body in bodies:
                first_of_body = set()
                prefix_nullable = True

                # (a) اگر A -> ε
                if body == ['ε']:
                    first_of_body = {'ε'}
                    prefix_nullable = True
                else:
                    # (b) محاسبهٔ FIRST(α)
                    for symbol in body:
                        if symbol in self.grammar.terminals:
                            first_of_body.add(symbol)
                            prefix_nullable = False
                            break
                        elif symbol in self.grammar.non_terminals:
                            first_of_body.update(self.first[symbol] - {'ε'})
                            if 'ε' in self.first[symbol]:
                                prefix_nullable = True
                            else:
                                prefix_nullable = False
                                break
                        else:
                            first_of_body.add(symbol)
                            prefix_nullable = False
                            break

                    if prefix_nullable:
                        first_of_body.add('ε')

                # (c) برای هر t ∈ FIRST(α) \ {ε}:
                for terminal in (first_of_body - {'ε'}):
                    self.parse_table[(head, terminal)] = body

                # (d) اگر ε ∈ FIRST(α)، برای هر t ∈ FOLLOW(head): جدول[head, t] = ['ε']
                if 'ε' in first_of_body:
                    for terminal in self.follow[head]:
                        self.parse_table[(head, terminal)] = ['ε']

        # ===== چاپ جدول برای T' و E' =====
        print("===== Parse Table for T' and E' =====")
        for nt in ["T'", "E'"]:
            for t in sorted(self.grammar.terminals.union({'$'})):
                prod = self.parse_table.get((nt, t))
                if prod is not None:
                    print(f"parse_table[({nt}, {t})] = {prod}")
        print("=====================================\n")

        return self.parse_table

    def display_parse_table(self):
        """
        نمایش جدول LL(1) به صورت ماتریس.
        """
        nts = sorted(self.grammar.non_terminals)
        terms = sorted(self.grammar.terminals.union({'$'}))

        header = ['NT/T'] + terms
        print(' | '.join(header))
        print('-' * (len(header) * 10))

        for nt in nts:
            row = [nt]
            for t in terms:
                prod = self.parse_table.get((nt, t))
                if prod:
                    row.append(' '.join(prod))
                else:
                    row.append('')
            print(' | '.join(row))

    def build_dpda_transitions(self):
        """
        ساخت ترانزیشن‌های DPDA بر اساس جدول LL(1).
        """
        transitions = {}
        state = 'q'
        accept_state = 'q_accept'

        # 1) تطابقِ ترمینال
        for t in self.grammar.terminals:
            transitions[(state, t, t)] = (state, [])

        # 2) گسترش غیرپایانه (با کلید = (state, lookahead, nonterminal))
        for nt in self.grammar.non_terminals:
            for t in self.grammar.terminals.union({'$'}):
                body = self.parse_table.get((nt, t))
                if body is not None:
                    action = [] if body == ['ε'] else body[:]
                    transitions[(state, t, nt)] = (state, action)

        # 3) پذیرش: وقتی lookahead = '$' و stack_top = 'ε'
        transitions[(state, '$', 'ε')] = (accept_state, [])

        states = {state, accept_state}
        input_symbols = set(self.grammar.terminals.union({'$'})).union({'ε'})
        stack_symbols = set(self.grammar.non_terminals.union(self.grammar.terminals)).union({'ε'})
        start_state = state
        start_stack_symbol = self.grammar.start_symbol
        accept_states = {accept_state}

        # ===== چاپ مختصر DPDA ساخته‌شده =====
        print("=== نمایش DPDA ساخته‌شده ===")
        print("=== DPDA Definition ===")
        print(f"States: {states}")
        print(f"Input Alphabet: {input_symbols}")
        print(f"Stack Alphabet: {stack_symbols}")
        print(f"Start State: {start_state}")
        print(f"Start Stack Symbol: {start_stack_symbol}")
        print(f"Accept States: {accept_states}\n")
        print("Transitions:")
        for key, val in transitions.items():
            st, la, top = key
            ns, action = val
            rhs = ' '.join(action) if action else 'ε'
            print(f"  δ({st}, {la}, {top}) = ({ns}, {rhs})")
        print("========================\n")

        return DPDA(states, input_symbols, stack_symbols, transitions,
                    start_state, start_stack_symbol, accept_states)
