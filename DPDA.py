class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def add_children(self, child_nodes):
        self.children = child_nodes

    def __repr__(self):
        return f"{self.symbol}"


class DPDA:
    def __init__(self, states, input_symbols, stack_symbols, transitions,
                 start_state, start_stack_symbol, accept_states):
        self.states = states
        self.input_symbols = input_symbols
        self.stack_symbols = stack_symbols
        self.transitions = transitions
        self.start_state = start_state
        self.start_stack_symbol = start_stack_symbol
        self.accept_states = accept_states
        self.parse_tree_root = None

    def display(self):
        print("=== DPDA Definition ===")
        print(f"States: {self.states}")
        print(f"Input Alphabet: {self.input_symbols}")
        print(f"Stack Alphabet: {self.stack_symbols}")
        print(f"Start State: {self.start_state}")
        print(f"Start Stack Symbol: {self.start_stack_symbol}")
        print(f"Accept States: {self.accept_states}")
        print("\nTransitions:")
        for key, value in sorted(self.transitions.items()):
            state, lookahead, stack_top = key
            next_state, action = value
            action_str = 'ε' if not action else ' '.join(action)
            print(f"  δ({state}, {lookahead}, {stack_top}) = ({next_state}, {action_str})")
        print("========================\n")

    def _print_tree(self, node, indent=0):
        print('  ' * indent + f"- {node.symbol}")
        for child in node.children:
            self._print_tree(child, indent + 1)

    def process_input(self, input_tokens):
        root_node = Node(self.start_stack_symbol)
        self.parse_tree_root = root_node
        stack = [self.start_stack_symbol]
        node_stack = [root_node]
        current_state = self.start_state
        input_index = 0

        print("=== شروع تجزیه ===")
        print(f"توکن‌ها: {input_tokens}")
        print(f"حالت اولیه: {current_state}")
        print("پشته اولیه (سمبل‌ها):", stack)
        print("پشته اولیه (گره‌های درخت):", [n.symbol for n in node_stack])
        print("----------------------------")

        step = 1
        while True:
            lookahead_real = input_tokens[input_index] if input_index < len(input_tokens) else '$'
            stack_top = stack[-1] if stack else 'ε'
            node_top = node_stack[-1] if node_stack else None

            print(f"مرحله {step}:")
            print(f"  حالت جاری: {current_state}")
            print(f"  پشته (سمبل‌ها): {stack}")
            print(f"  پشته (گره‌ها): {[n.symbol for n in node_stack]}")
            print(f"  سمبل ورودی (lookahead_real): {lookahead_real}")

            if stack_top in self.input_symbols and stack_top == lookahead_real:
                key_match = (current_state, lookahead_real, stack_top)
                if key_match in self.transitions:
                    next_state, _ = self.transitions[key_match]
                    stack.pop()
                    node_stack.pop()
                    input_index += 1
                    current_state = next_state
                    step += 1
                    print("  -> تطابق ترمینال")
                    print("----------------------------")
                    continue

            if stack_top != 'ε' and stack_top not in self.input_symbols:
                key_expand = (current_state, lookahead_real, stack_top)
                key_eps = (current_state, 'ε', stack_top)
                used_key = key_expand if key_expand in self.transitions else key_eps if key_eps in self.transitions else None

                if used_key:
                    next_state, action = self.transitions[used_key]
                    stack.pop()
                    parent = node_stack.pop()
                    if action:
                        children = [Node(sym) for sym in action]
                        parent.add_children(children)
                        for child in reversed(children):
                            stack.append(child.symbol)
                            node_stack.append(child)
                    else:
                        parent.add_children([])
                    current_state = next_state
                    step += 1
                    print("  -> گسترش غیرپایانه")
                    print("----------------------------")
                    continue

            if stack_top == 'ε' and lookahead_real == '$':
                key_accept = (current_state, '$', 'ε')
                if key_accept in self.transitions:
                    current_state = self.transitions[key_accept][0]
                    break

            print("هیچ ترانزیشنی یافت نشد.")
            break

        print(f"حالت نهایی: {current_state}")
        if current_state in self.accept_states and input_index == len(input_tokens):
            print("✅ نتیجه: رشته پذیرفته شد.\n")
            return True, self.parse_tree_root
        else:
            print("❌ نتیجه: رشته پذیرفته نشد.\n")
            return False, None

    def rename_symbol_in_tree(self, old_name, new_name):
        if self.parse_tree_root is None:
            print("⚠️ درخت تجزیه هنوز ساخته نشده است.")
            return

        def dfs_rename(node):
            if node.symbol == old_name:
                node.symbol = new_name
            for child in node.children:
                dfs_rename(child)

        dfs_rename(self.parse_tree_root)
        print(f"✅ همه گره‌های با نماد '{old_name}' به '{new_name}' تغییر یافتند.")