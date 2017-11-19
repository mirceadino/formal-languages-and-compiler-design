from fa.finite_automata import FiniteAutomata


class FiniteAutomataFromFile(FiniteAutomata):
    def __init__(self, filename):
        with open(filename) as f:
            file_lines = list(f)
            states = file_lines[0].split()
            alphabet = list(file_lines[1].strip())
            initial_state = file_lines[2].strip()
            accepted_states = file_lines[3].split()
            file_lines = file_lines[4:]
            transitions = []
            for line in file_lines:
                transitions.append(line.strip().split())
        super().__init__(states, alphabet, initial_state, accepted_states)
        for transition in transitions:
            for char in transition[1]:
                super().set_transition(transition[0], char, transition[2])


if __name__ == "__main__":
    b = FiniteAutomataFromFile("identifier.txt")
    print(b.check("fejfoe"))
