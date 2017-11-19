

class FiniteAutomata:
    def __init__(self, states=[], alphabet=[], initial_state=None, accepted_states=[]):
        self.states = states
        self.alphabet = alphabet
        assert(initial_state in self.states)
        self.initial_state = initial_state
        for state in accepted_states:
            assert(state in self.states)
        self.accepted_states = accepted_states
        self.transitions = {}
        for state in self.states:
            self.transitions[state] = {}

    def add_state(self, state):
        assert(state not in self.states)
        self.states.append(state)
        self.transitions[state] = {}

    def add_char(self, char):
        assert(char not in self.alphabet)
        self.alphabet.append(char)

    def set_transition(self, source, char, destination):
        assert(source in self.states)
        assert(char in self.alphabet)
        assert(destination in self.states)
        self.transitions[source][char] = destination

    def set_initial_state(self, state):
        assert(state in self.states)
        self.initial_state(state)

    def add_accepted_state(self, state):
        assert(state in self.accepted_states)
        self.accepted_states.append(state)

    def check(self, sequence):
        for char in sequence:
            if char not in self.alphabet:
                return False
        current = self.initial_state
        for char in sequence:
            if char not in self.transitions[current]:
                return False
            current = self.transitions[current][char]
        return current in self.accepted_states

    def determine_longest_prefix(self, sequence):
        current = self.initial_state
        longest_prefix = ""
        for char in sequence:
            if char not in self.transitions[current]:
                return longest_prefix
            current = self.transitions[current][char]
            longest_prefix += char
        return longest_prefix

