# Deterministic Finite Automaton (DFA) with modularization
# Accept strings with final character 1 and reject strings with final characters 0

# States (Q): A finite set of states. Example: {q0, q1}
# Alphabet (Σ): A finite set of input symbols. Example: {0, 1} 
# Transition Function (δ): A function mapping (current_state, input_symbol) → next_state. Example: q0, 0, q0; q0, 1, q1; q1, 0, q0; q1, 1, q1;
# Start State (q0): The state where the DFA begins. Example: q0
# Accept States (F): A subset of Q that represents accepting states. Example: q1

# Dfa Class
class Dfa:
    # Constructor
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state 

    def transition(self, symbol):
        if (self.current_state, symbol) in self.transitions:
            self.current_state = self.transitions[(self.current_state, symbol)]
        else:
            raise ValueError(f"No transition defined for ({self.current_state}, {symbol})")

    def process_input(self, input_string):
        self.current_state = self.start_state 
        for symbol in input_string:
            self.transition(symbol)
        return self.current_state in self.accept_states 

# Dfa Example
states = {"q0", "q1"}
alphabet = {"0", "1"}
transitions = {("q0", "0"): "q0", ("q0", "1"): "q1", ("q1", "0"): "q0", ("q1", "1"): "q1"}
start_state = "q0"
accept_states = {"q1"}

dfa_instance = Dfa(states, alphabet, transitions, start_state, accept_states)

test_cases = ["0", "1", "01", "10", "111", "100"]
for test in test_cases:
    result = dfa_instance.process_input(test)
    print(f"Input: {test} → {'Accepted' if result else 'Rejected'}")
