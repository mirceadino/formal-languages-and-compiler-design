from grammar_factory import GrammarFactory
from parser import *
from sys import argv


def main_wikipedia():
    grammar = GrammarFactory.wikipedia()
    print(grammar)

    parsing_table = ParsingTable(grammar)
    print(parsing_table)

    parser = LL1Parser(parsing_table)
    stream = ["(", "a", "+", "a", ")"]
    stack = ["S"]
    derivations = parser.parse(stream, stack)

    for rule in derivations:
        print(str(rule))


def read_from_file():
    filename = argv[1]
    f = open(filename)
    stream = []
    for line in f:
        token = line.strip()
        stream.append(token)
    return stream


def main_mlp():
    grammar = GrammarFactory.mlp()
    print(grammar)

    parsing_table = ParsingTable(grammar)
    print(parsing_table)

    parser = LL1Parser(parsing_table)
    stream = read_from_file()
    stack = ["program"]
    derivations = parser.parse(stream, stack)

    for rule in derivations:
        print(str(rule))


def main():
    if len(argv) <= 1:
        main_wikipedia()
    else:
        main_mlp()


if __name__ == "__main__":
    main()
