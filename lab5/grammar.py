
class Token:
    def __init__(self, name, is_terminal=False):
        # name: str
        # is_terminal: bool
        self.name = name
        self.is_terminal = is_terminal

    def __str__(self):
        return repr(self)
        # return "{0}(\'{1}\')]".format("Terminal" if self.is_terminal else "Non-terminal", self.name)

    def __repr__(self):
        return "{0}".format(self.name)


class Rule:
    def __init__(self, lhs, rhs):
        # lhs: non-terminal Token
        # rhs: list of Tokens (both terminal and non-terminal)
        self.id = 0
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return repr(self.id)

    def __str__(self):
        r = "#{0}. {1} -> ".format(self.id, self.lhs)
        for token in self.rhs:
            r += str(token) + " "
        r = r[:-1]
        return r


class Grammar:
    def __init__(self):
        self.tokens = {}
        self.rules = {}

    def add_token(self, name, is_terminal=False):
        token = Token(name, is_terminal)
        self.tokens[name] = token

    def add_tokens(self, names, is_terminal=False):
        tokens = list(map(lambda x: Token(x, is_terminal), names))
        for token in tokens:
            self.tokens[token.name] = token

    def add_rule(self, lhs, rhs):
        rule = Rule(self.tokens[lhs], list(map(lambda x: self.tokens[x], rhs)))
        rule.id = len(self.rules) + 1
        self.rules[rule.id] = rule

    def terminal_tokens(self):
        return list(filter(lambda x: x.is_terminal, self.all_tokens()))

    def non_terminal_tokens(self):
        return list(filter(lambda x: not x.is_terminal, self.all_tokens()))

    def all_tokens(self):
        return sorted(list(self.tokens.values()), key=lambda x: x.name)

    def all_rules(self):
        return sorted(list(self.rules.values()), key=lambda x: x.id)

    def rules_for(self, token_name):
        return list(filter(lambda x: x.lhs.name is token_name, self.rules.values()))

    def __str__(self):
        r = "  Grammar:\n"
        r += "Terminal tokens: {0}\n".format(self.terminal_tokens())
        r += "Non-terminal tokens: {0}\n".format(self.non_terminal_tokens())
        r += "Rules:\n"
        for rule in self.all_rules(): 
            r += str(rule) + '\n'
        r += "-----"
        return r
