from grammar_factory import GrammarFactory
from parser import *


def main():
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


if __name__ == "__main__":
    main()
