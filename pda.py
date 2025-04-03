# Pushdown Automaton (PDA) for aⁿbⁿ
class Pda:
    def __init__(self, states, alphabet, stack_alphabet, transitions, start_state, accept_states, start_stack_symbol):
        self.states = states  # Finite set of states
        self.alphabet = alphabet  # Input symbols
        self.stack_alphabet = stack_alphabet  # Stack symbols
        self.transitions = transitions  # Transition function
        self.start_state = start_state  # Initial state
        self.accept_states = accept_states  # Accepting states
        self.stack = [start_stack_symbol]  # Stack initialized with start symbol
        self.current_state = start_state  # Start state

    def transition(self, symbol):
        if (self.current_state, symbol, self.stack[-1]) in self.transitions:
            next_state, stack_action = self.transitions[(self.current_state, symbol, self.stack[-1])]

            # Stack operations
            if stack_action == "POP":
                self.stack.pop()  # Remove top element
            elif stack_action != "ε":  # If not ε (do nothing), push symbol
                self.stack.append(stack_action)

            # Move to next state
            self.current_state = next_state
        else:
            return False  # Reject if no valid transition

    def process_input(self, input_string):
        self.current_state = self.start_state
        self.stack = ["Z"]  # Reset stack

        for symbol in input_string:
            if self.transition(symbol) is False:
                return False  # Reject if transition fails

        # Accept if the stack is empty (ensuring equal a's and b's)
        return self.current_state in self.accept_states and len(self.stack) == 1

# Define PDA components
states = {"q0", "q1", "qf"}
alphabet = {"a", "b"}
stack_alphabet = {"Z", "A"}  # Stack can hold 'Z' (start symbol) or 'A'
transitions = {
    # Push 'A' for each 'a' encountered
    ("q0", "a", "Z"): ("q0", "A"),
    ("q0", "a", "A"): ("q0", "A"),

    # Switch to consuming 'b's when we see the first 'b'
    ("q0", "b", "A"): ("q1", "POP"),  # Pop A when encountering first b

    # Continue consuming 'b's and popping 'A's
    ("q1", "b", "A"): ("q1", "POP"),

    # Accept if stack is empty after matching a's with b's
    ("q1", "ε", "Z"): ("qf", "ε")  # Final transition
}

start_state = "q0"
accept_states = {"qf"}
start_stack_symbol = "Z"

# Initialize PDA
pda_instance = Pda(states, alphabet, stack_alphabet, transitions, start_state, accept_states, start_stack_symbol)

# Test cases
test_cases = ["ab", "aabb", "aaabbb", "aaaaabbbbb", "a", "b", "abb", "aab", "ba", "abab"]
for test in test_cases:
    result = pda_instance.process_input(test)
    print(f"Input: {test} → {'Accepted' if result else 'Rejected'}")
