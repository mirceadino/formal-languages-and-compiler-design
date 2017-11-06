from finite_automata import FiniteAutomata
from string import ascii_lowercase
import sys


def main():
    if len(sys.argv) < 2:
        print("usage: {0} <file>".format(sys.argv[0]))
        return

    filename = sys.argv[1]
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
    fa = FiniteAutomata(states, alphabet, initial_state, accepted_states)
    for transition in transitions:
        for char in transition[1]:
            fa.set_transition(transition[0], char, transition[2])

    do_option = {}
    do_option["1"] = show_states
    do_option["2"] = show_alphabet
    do_option["3"] = show_transitions
    do_option["4"] = show_initial_state
    do_option["5"] = show_accepted_states
    do_option["6"] = check_sequence
    do_option["7"] = determine_longest_prefix
    while True:
        print_menu()
        option = input("Type option: ").strip()
        if option is "0":
            break
        else:
            do_option[option](fa)


def print_menu():
    print("1 - Show states")
    print("2 - Show alphabet")
    print("3 - Show transitions")
    print("4 - Show initial state")
    print("5 - Show accepted states")
    print("6 - Check sequence")
    print("7 - Determine longest prefix")
    print("0 - Exit")


def show_states(fa):
    print(fa.states)


def show_alphabet(fa):
    print(fa.alphabet)


def show_transitions(fa):
    for state in fa.states:
        print("state {0}: {1}".format(state, str(fa.transitions[state])))


def show_initial_state(fa):
    print(fa.initial_state)


def show_accepted_states(fa):
    print(fa.accepted_states)


def check_sequence(fa):
    sequence = list(input("Type sequence: ").strip())
    print(fa.check(sequence))


def determine_longest_prefix(fa):
    sequence = list(input("Type sequence: ").strip())
    print("\"{0}\"".format(fa.determine_longest_prefix(sequence)))


if __name__ == '__main__':
    main()

