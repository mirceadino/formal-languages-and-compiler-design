from grammar import *


class GrammarFactory:
    @staticmethod
    def wikipedia():
        grammar = Grammar()
        grammar.add_tokens(["S", "F"])
        grammar.add_tokens(["a", "(", ")", "+"], True)
        grammar.add_rule("S", ["F"])
        grammar.add_rule("S", ["(", "S", "+", "F", ")"])
        grammar.add_rule("F", ["a"])
        return grammar

    @staticmethod
    def mlp():
        grammar = Grammar()

        grammar.add_tokens(["program", \
                           "declaration_list", \
                           "statement_list", \
                           "variable_declaration", \
                           "statement", \
                           "assignment_statement", \
                           "io_statement", \
                           "if_statement", \
                           "expression", \
                           "term", \
                           "expression_rest", \
                           "add_sub_operator", \
                           "factor", \
                           "term_rest", \
                           "mul_div_mod_operator", \
                           "numeral", \
                           "read_statement", \
                           "write_statement", \
                           "condition", \
                           "while_statement", \
                           "else_branch"]);

        grammar.add_tokens([";", \
                            "=", \
                            "(", ")",
                            "{", "}",
                            "TYPE", \
                            "IDENTIFIER", \
                            "ADD", \
                            "SUBSTRACT", \
                            "MULTIPLY", \
                            "DIVIDE", \
                            "MODULO", \
                            "CONSTANT", \
                            "CIN", \
                            "COUT", \
                            "CIN_OP", \
                            "COUT_OP", \
                            "IF", \
                            "ELSE", \
                            "WHILE", \
                            "BOOL"], True)

        grammar.add_rule("program", ["declaration_list", "statement_list"])
        grammar.add_rule("declaration_list", [])
        grammar.add_rule("declaration_list", ["variable_declaration", "declaration_list"])
        grammar.add_rule("variable_declaration", ["TYPE", "IDENTIFIER", ";"])
        grammar.add_rule("statement_list", [])
        grammar.add_rule("statement_list", ["statement", "statement_list"])
        grammar.add_rule("statement", ["assignment_statement", ";"])
        grammar.add_rule("statement", ["io_statement", ";"])
        grammar.add_rule("statement", ["if_statement", ";"])
        grammar.add_rule("statement", ["while_statement"])
        grammar.add_rule("assignment_statement", ["IDENTIFIER", "=", "expression"])
        grammar.add_rule("expression", ["term", "expression_rest"])
        grammar.add_rule("expression_rest", [])
        grammar.add_rule("expression_rest", ["add_sub_operator", "expression"])
        grammar.add_rule("add_sub_operator", ["ADD"])
        grammar.add_rule("add_sub_operator", ["SUBSTRACT"])
        grammar.add_rule("term", ["factor", "term_rest"])
        grammar.add_rule("term_rest", [])
        grammar.add_rule("term_rest", ["mul_div_mod_operator", "term"])
        grammar.add_rule("mul_div_mod_operator", ["MULTIPLY"])
        grammar.add_rule("mul_div_mod_operator", ["DIVIDE"])
        grammar.add_rule("mul_div_mod_operator", ["MODULO"])
        grammar.add_rule("factor", ["numeral"])
        grammar.add_rule("factor", ["(", "expression", ")"])
        grammar.add_rule("numeral", ["CONSTANT"])
        grammar.add_rule("numeral", ["IDENTIFIER"])
        grammar.add_rule("io_statement", ["read_statement"])
        grammar.add_rule("io_statement", ["write_statement"])
        grammar.add_rule("read_statement", ["CIN", "CIN_OP", "IDENTIFIER"])
        grammar.add_rule("write_statement", ["COUT", "COUT_OP", "numeral"])
        grammar.add_rule("if_statement", ["IF", "(", "condition", ")", "{", "statement_list", "}", "else_branch"])
        grammar.add_rule("else_branch", [])
        grammar.add_rule("else_branch", ["ELSE", "{", "statement_list", "}"])
        grammar.add_rule("condition", ["expression", "BOOL", "expression"])
        grammar.add_rule("while_statement", ["WHILE", "(", "condition", ")", "{", "statement_list", "}"]);
        return grammar
