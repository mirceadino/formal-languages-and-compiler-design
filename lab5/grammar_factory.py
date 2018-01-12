from grammar import *


class GrammarFactory:
    @staticmethod
    def wikipedia():
        grammar = Grammar()
        grammar.add_token("S")
        grammar.add_token("F")
        grammar.add_token("a", True)
        grammar.add_token("(", True)
        grammar.add_token(")", True)
        grammar.add_token("+", True)
        grammar.add_rule("S", ["F"])
        grammar.add_rule("S", ["(", "S", "+", "F", ")"])
        grammar.add_rule("F", ["a"])
        return grammar
