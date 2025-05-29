class DPDA:
    def __init__(self, states, input_symbols, stack_symbols, transitions,
                 start_state, start_stack_symbol, accept_states):
        self.states = states
        self.input_symbols = input_symbols
        self.stack_symbols = stack_symbols
        self.transitions = transitions  # dict: (state, input_symbol, stack_top) -> (next_state, stack_action)
        self.start_state = start_state
        self.start_stack_symbol = start_stack_symbol
        self.accept_states = accept_states

    def process_input(self, input_string):
        stack = [self.start_stack_symbol]
        current_state = self.start_state
        input_index = 0

        while True:
            input_symbol = input_string[input_index] if input_index < len(input_string) else 'ε'
            stack_top = stack[-1] if stack else 'ε'
            key = (current_state, input_symbol, stack_top)

            if key in self.transitions:
                next_state, stack_action = self.transitions[key]
                current_state = next_state

                # انجام عملیات پشته
                if stack:
                    stack.pop()
                if stack_action != 'ε':
                    for symbol in reversed(stack_action):
                        stack.append(symbol)

                if input_symbol != 'ε':
                    input_index += 1
            else:
                break

        return current_state in self.accept_states and (input_index == len(input_string))
