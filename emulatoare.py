# Cerinta: Scrie cate un emultator pentru DFA, NFA, PDA si Turing Machine
# Nume: Irimia David
# Grupa: 141
# Nota: Fisierele de input (dfa.txt, nfa.txt, pda.txt, tm.txt) au fost adaugate si la finalul fisierului sub forma de comentarii

################
# DFA Emulator #
################

class DFA:
    # Constructorul clasei primeste: multimea starilor, alfabetul, tranzitiile, starea de inceput, starea de final
    def __init__(self, states, alphabet, transitions, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start = start
        self.accept = accept

    # Verifica daca un sir de intrare este acceptat
    def process(self, input_str):

        # Pornim cu starea de inceput
        state = self.start
        
        # Pentru fiecare simbol din sir, daca nu exista tranzitie atunci respingem sirul
        for symbol in input_str:
            state = self.transitions.get((state, symbol))
            if state is None:
                return False
        return state in self.accept

################
# NFA Emulator #
################

class NFA:
    # Constructorul clasei primeste: multimea starilor, alfabetul, tranzitiile, starea de inceput, starea de final
    def __init__(self, states, alphabet, transitions, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accept = accept
    
    # Calculeaza inchiderea unui set de stari (adica starile la care putem ajunge prin tranzitii epsilon)
    def epsilon_closure(self, states):
        
        # Initial epsilon_closure contine starile de pornire
        stack = list(states)
        closure = set(states)

        # Repeta cat timp putem gasi noi stari prin tranzitii epsilon
        while stack:
            state = stack.pop()
            for next_state in self.transitions.get((state, ''), set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    # Verifica daca un sir de intrare este acceptat
    def process(self, input_str):

        # Pornim cu inchiderea epsilon a starii de start
        current_states = self.epsilon_closure({self.start})
        
        # Pentru fiecare simbol din input vedem in ce stari putem ajunge si aplicam din nou epsilon_closure
        for symbol in input_str:
            next_states = set()
            for state in current_states:
                next_states |= self.transitions.get((state, symbol), set())
            current_states = self.epsilon_closure(next_states)
        
        # Accepta doar daca cel putin o stare curenta este de acceptare
        return bool(current_states & self.accept)

################
# PDA Emulator #
################

class PDA:
    # Constructorul clasei primeste: multimea starilor, alfabetul, alfabetul stivei, tranzitiile, starea de inceput, starea de final
    def __init__(self, states, alphabet, stack_alphabet, transitions, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions 
        self.start = start
        self.accept = accept
    
    # Verifica daca un sir de intrare este acceptat
    def process(self, input_str):
        
        # Initializeaza stiva cu $
        stack = ['$']

        # Retine toate configuratiile posibile
        configurations = [(self.start, 0, stack)]
        
        # Exploraeaza configuratiile pe rand, una cate una
        while configurations:
            state, index, stack = configurations.pop()
            stack_top = stack[-1] if stack else ''
            symbol = input_str[index] if index < len(input_str) else ''
            
            # Cauta tranzitii valide
            for (s, a, t), actions in self.transitions.items():
                if s == state and (a == symbol or a == '') and (t == stack_top or t == ''):
                    for (new_state, stack_ops) in actions:
                        new_stack = stack.copy()
                        if t != '': new_stack.pop()
                        for char in reversed(stack_ops):
                            if char != '': new_stack.append(char)
                        new_index = index + (1 if a != '' else 0)
                        if new_state in self.accept and new_index == len(input_str):
                            return True
                        configurations.append((new_state, new_index, new_stack))
        return False

###########################
# Turing Machine Emulator #
###########################

class TuringMachine:
    # Constructorul clasei primeste: multimea starilor, alfabetul, sfarsitul sirului de intrare, tranzitiile, starea de inceput, starea de final
    def __init__(self, states, tape_alphabet, blank, transitions, start, accept):
        self.states = states
        self.tape_alphabet = tape_alphabet
        self.blank = blank
        self.transitions = transitions 
        self.start = start
        self.accept = accept
    
    # Verifica daca un sir de intrare este acceptat
    def process(self, input_str):
        
        # Creeaza banda si adauga un spatiu liber (acel blank) la final
        tape = list(input_str) + [self.blank]
        head = 0
        state = self.start
        
        # Repeta cat timp exista o tranzitie definita pentru (state, symbol)
        while True:
            symbol = tape[head] if head < len(tape) else self.blank
            if (state, symbol) not in self.transitions:
                break

            # Scrie simbolul pe banda si actualizeaza starea
            new_state, write_symbol, direction = self.transitions[(state, symbol)]
            tape[head] = write_symbol
            state = new_state
            if direction == 'R':
                head += 1
                if head >= len(tape): tape.append(self.blank)
            elif direction == 'L':
                head = max(0, head - 1)
        return state in self.accept

################################
# File loader for all automata #
################################

# Citeste fisierul ignorand liniile goale si comentariile
def load_automaton(file_path):
    with open(file_path) as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Citeste o sectiune delimitata de [{name}] si [End] unde {name} poate fi: States, Alphabet, Transitions, Start, Accept
    def read_section(name):
        idx = lines.index(f"[{name}]") + 1
        end = lines.index("[End]", idx)
        return lines[idx:end]
    
    # Extrage toate componentele automatului
    states = set(read_section("States"))
    alphabet = set(read_section("Alphabet"))
    start = read_section("Start")[0]
    accept = set(read_section("Accept"))
    transitions_raw = read_section("Transitions")

    # Returnam componentele automatului
    return states, alphabet, start, accept, transitions_raw

######################
# Main testing block #
######################

if __name__ == "__main__":

    ############
    # DFA Test #
    ############

    # Incarca din fisier: starile, alfabetul, starea de inceput, starea de final si tranzitiile
    states, alphabet, start, accept, raw_trans = load_automaton("dfa.txt")
    
    # Construieste dictionarul de tranzitii
    dfa_transitions = {}
    for line in raw_trans:
        src, sym, dst = map(str.strip, line.split(","))
        dfa_transitions[(src, sym)] = dst
    
    # Creeaza obiect
    dfa = DFA(states, alphabet, dfa_transitions, start, accept)
    
    # Verifica sirurile de test daca sunt acceptate sau daca sunt respinse
    print("DFA:")
    for test in ["0", "1", "01", "10", "111", "100"]:
        print(f"{test} → {'Accepted' if dfa.process(test) else 'Rejected'}")

    ############
    # NFA Test #
    ############

    # Incarca din fisier: starile, alfabetul, starea de inceput, starea de final si tranzitiile
    states, alphabet, start, accept, raw_trans = load_automaton("nfa.txt")
    
    # Construieste dictionarul de tranzitii
    nfa_transitions = {}
    for line in raw_trans:
        src, sym, *dests = map(str.strip, line.split(","))
        nfa_transitions.setdefault((src, sym), set()).update(dests)
    
    # Creeaza obiect
    nfa = NFA(states, alphabet, nfa_transitions, start, accept)
    
    # Verifica sirurile de test daca sunt acceptate sau daca sunt respinse
    print("\nNFA:")
    for test in ["", "a", "ab", "aba", "aab"]:
        print(f"{test} → {'Accepted' if nfa.process(test) else 'Rejected'}")

    ############
    # PDA Test #
    ############

    # Incarca din fisier: starile, alfabetul, starea de inceput, starea de final si tranzitiile
    states, alphabet, start, accept, raw_trans = load_automaton("pda.txt")
    stack_alphabet = {'$', 'A'}

    # Construieste dictionarul de tranzitii
    pda_transitions = {}
    for line in raw_trans:
        src, sym, stack_top, dst, stack_push = map(str.strip, line.split(","))
        pda_transitions.setdefault((src, sym, stack_top), []).append((dst, list(stack_push)))
    
    # Construieste obiectul
    pda = PDA(states, alphabet, stack_alphabet, pda_transitions, start, accept)
    
    # Verifica sirurile de test daca sunt acceptate sau daca sunt respinse
    print("\nPDA:")
    for test in ["", "ab", "aabb", "aaabbb", "aab"]:
        print(f"{test} → {'Accepted' if pda.process(test) else 'Rejected'}")

    #######################
    # Turing Machine Test #
    #######################
    
    # Incarca din fisier: starile, alfabetul, starea de inceput, starea de final si tranzitiile
    states, alphabet, start, accept, raw_trans = load_automaton("tm.txt")
    tape_alphabet = alphabet | {'_'}
    blank = '_'
    
    # Construieste dictionarul de tranzitii
    tm_transitions = {}
    for line in raw_trans:
        src, read, dst, write, direction = map(str.strip, line.split(","))
        tm_transitions[(src, read)] = (dst, write, direction)
    
    # Construieste obiectul
    tm = TuringMachine(states, tape_alphabet, blank, tm_transitions, start, accept)
    
    # Verifica sirurile de test daca sunt acceptate sau daca sunt respinse
    print("\nTuring Machine:")
    for test in ["", "a", "aa", "aaa"]:
        print(f"{test} → {'Accepted' if tm.process(test) else 'Rejected'}")

###########
# dfa.txt #
###########

# [States]
# q0
# q1
# [End]

# [Alphabet]
# 0
# 1
# [End]

# [Start]
# q0
# [End]

# [Accept]
# q1
# [End]

# [Transitions]
# q0,0,q0
# q0,1,q1
# q1,0,q0
# q1,1,q1
# [End]

###########
# nfa.txt #
###########

# [States]
# q0
# q1
# q2
# [End]

# [Alphabet]
# 0
# 1
# [End]

# [Start]
# q0
# [End]

# [Accept]
# q2
# [End]

# [Transitions]
# q0,0,q0
# q0,1,q0
# q0,1,q1
# q1,1,q2
# [End]

###########
# pda.txt #
###########

# [States]
# q0
# q1
# q2
# [End]

# [Alphabet]
# a
# b
# [End]

# [Start]
# q0
# [End]

# [Accept]
# q2
# [End]

# [Transitions]
# q0, a, $, q0, A$
# q0, a, A, q0, AA
# q0, b, A, q1, ε
# q1, b, A, q1, ε
# q1, ε, $, q2, ε
# [End]

##########
# tm.txt #
##########

# [States]
# q0
# q1
# q_accept
# [End]

# [Alphabet]
# a
# [End]

# [Start]
# q0
# [End]

# [Accept]
# q_accept
# [End]

# [Transitions]
# q0, a, q1, a, R
# q1, a, q0, a, R
# q0, _, q_accept, _, R
# [End]
