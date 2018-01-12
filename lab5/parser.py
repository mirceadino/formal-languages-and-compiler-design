from grammar import *


class ParsingTable:
    def __init__(self, grammar):
        self.grammar = grammar
        self.rules = {}
        self._build()

    def _left_terminals(self, token):
        if token.is_terminal:
            return [token]
        all_left_terminals = []
        for rule in self.grammar.rules_for(token.name):
            left_token = rule.rhs[0]
            all_left_terminals += self._left_terminals(left_token)
        return all_left_terminals
    
    def _build(self):
        grammar = self.grammar
        for non_terminal in grammar.non_terminal_tokens():
            self.rules[non_terminal.name] = {}
            for terminal in grammar.terminal_tokens():
                self.rules[non_terminal.name][terminal.name] = None
            for rule in grammar.rules_for(non_terminal.name):
                for terminal in self._left_terminals(rule.rhs[0]):
                    self.rules[non_terminal.name][terminal.name] = rule

    def rule(self, non_terminal_name, terminal_name):
        try:
            return self.rules[non_terminal_name][terminal_name]
        except KeyError:
            return None

    def __repr__(self):
        r = "  Parsing table:\n"
        grammar = self.grammar
        for non_terminal in grammar.non_terminal_tokens():
            r += "{0} : {1}\n".format(non_terminal.name, self.rules[non_terminal.name])
        r += "----"
        return r


class LL1Parser:
    def __init__(self, parsing_table):
        self.parsing_table = parsing_table

    def parse(self, stream, stack):
        derivations = []
        num_steps = 0
        while len(stream) != 0 and len(stack) != 0:
            print("  Step #{0}".format(num_steps))
            print("Stream: {0}".format(stream))
            print("Stack: {0}".format(stack))
            from_stream = stream[0]
            from_stack = stack[0]
            stack = stack[1:]
            if from_stream is from_stack:
                stream = stream[1:]
            else:
                rule = self.parsing_table.rule(from_stack, from_stream)
                if rule is not None:
                    print("Applying: {0}".format(str(rule)))
                    derivations.append(rule)
                    stack = list(map(lambda x: x.name, rule.rhs)) + stack
                else:
                    print("Error. Parsing halted.")
                    derivations = []
                    break
            num_steps += 1
            print("-----")
        if len(stream) != 0 and len(stack) is 0:
            print("Error. Stack is empty.")
            derivations = []
        return derivations
