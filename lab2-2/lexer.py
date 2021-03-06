import re
from fa.finite_automata_from_file import FiniteAutomataFromFile


class LexicalError:
    def __init__(self, token, context, line, message):
        self.token = token
        self.context = context
        self.message = message
        self.line = line

    def __repr__(self):
        return "{0}: {1} on line {2}: \"{3}\"".format(\
                self.token, self.message, self.line, self.context)


class Token:
    def __init__(self, tip, content, context, line=-1):
        self.type = tip
        self.content = content
        self.context = context
        self.line = line

    def __repr__(self):
        return "[{0}, {1}, line {2}]\n".format( \
                self.type, self.content, self.line)


class Lexer:
    kSeparator = 'SEPARATOR'
    kOperator = 'OPERATOR'
    kReserved = 'RESERVED'
    kConstant = 'CONSTANT'
    kIdentifier = 'IDENTIFIER'
    kSeparatorList = [';', '(', ')', '{', '}', "\""]
    kSimpleOperatorList = ['<', '>', '=', '+', '-', '*', '/', '%']
    kComposedOperatorList = ['<=', '>=', '==', '!=', '>>', '<<']
    kOperatorList = kSimpleOperatorList + kComposedOperatorList
    kReservedList = ['int', 'double', 'string', 'if', 'else', 'while', 'cin', 'cout']
    kPlaceholder = '$$#@@#'
    kAutomataIdentifier = FiniteAutomataFromFile("fa/identifier.txt")
    kAutomataIntConst = FiniteAutomataFromFile("fa/int_const.txt")
    kAutomataDoubleConst = FiniteAutomataFromFile("fa/double_const.txt")

    @staticmethod
    def is_constant(token):
        return Lexer.is_constant_int(token) or Lexer.is_constant_double(token)

    @staticmethod
    def is_constant_int(token):
        return Lexer.kAutomataIntConst.check(token)
        # return re.match("^[+-]?[0-9]+$", token) != None

    @staticmethod
    def is_constant_double(token):
        return Lexer.kAutomataDoubleConst.check(token)
        # return Lexer.is_constant_int(token) or \
        #        re.match("^[+-]?[0-9]+\.[0-9]+$", token) != None

    @staticmethod
    def is_identifier(token):
        return Lexer.kAutomataIdentifier.check(token)
        # return re.match("^[a-zA-Z_][a-zA-Z_0-9]*$", token) != None

    def Start(self, source):
        self._errors = []
        source = self._Preprocess(source)
        raw_tokens = self._Tokenize(source)
        tokens = self._LabelTokens(raw_tokens)
        # print(tokens)
        tokens = self._CheckTokens(tokens)
        self._st = self._BuildSymbolTable(tokens)
        self._pif = self._BuildProgramInternalForm(tokens)
        return self._st, self._pif, self._errors

    def _RecordError(self, token, context, line, message):
        self._errors.append(LexicalError(token, context, line, message))

    def _Preprocess(self, source):
        if len(self._errors) != 0:
            return
        # Replace composed operators with placeholders and add spaces around them.
        composed_operator_to_placeholder = {}
        for operator in Lexer.kComposedOperatorList:
            composed_operator_to_placeholder[operator] = \
                    Lexer.kPlaceholder + str(len(composed_operator_to_placeholder))
            source = source.replace(operator, \
                    ' ' + composed_operator_to_placeholder[operator] + ' ')
        # Add spaces around kSimpleOperatorList and kSeparatorList to easily tokenize.
        for char in Lexer.kSimpleOperatorList + Lexer.kSeparatorList:
            source = source.replace(char, ' ' + char + ' ')
        # Return to the composed operators.
        for operator in Lexer.kComposedOperatorList:
            source = source.replace(composed_operator_to_placeholder[operator], operator)
        # Replace newlines with a special character.
        source = source.replace('\n', ' ' + Lexer.kPlaceholder + ' ')
        return source

    def _Tokenize(self, source):
        if len(self._errors) != 0:
            return
        return source.split()

    def _LabelTokens(self, raw_tokens):
        if len(self._errors) != 0:
            return
        tokens = []
        line = 1
        context = ''
        for token in raw_tokens:
            if token == Lexer.kPlaceholder:
                line += 1
                context = ''
                continue
            context += token + ' '
            if token in Lexer.kSeparatorList:
                tokens.append(Token(Lexer.kSeparator, token, context, line))
            elif token in Lexer.kOperatorList:
                tokens.append(Token(Lexer.kOperator, token, context, line))
            elif token in Lexer.kReservedList:
                tokens.append(Token(Lexer.kReserved, token, context, line))
            elif Lexer.is_constant(token):
                ## We deal with negative and positive signs as part of 
                ## constants, not as operators.
                #if len(tokens) > 2 and \
                #    tokens[-1].type is Lexer.kOperator and \
                #    tokens[-1].content in ['-', '+'] and \
                #    tokens[-2].type is Lexer.kOperator and \
                #    tokens[-2].content in ['(', '=']:
                #        if tokens[-1].content is '-':
                #            token = tokens[-1].content + token
                #        tokens.pop()
                tokens.append(Token(Lexer.kConstant, token, context, line))
            elif Lexer.is_identifier(token):
                tokens.append(Token(Lexer.kIdentifier, token, context, line))
            else:
                self._RecordError(token, context, line, "not an identifier")
        return tokens

    def _CheckTokens(self, tokens):
        if len(self._errors) != 0:
            return
        for token in tokens:
            if token.type is Lexer.kIdentifier:
                if len(token.content) > 8:
                    self._RecordError(token.content, token.context, token.line, "identifier is too long (max 8 chars)")
        return tokens

    def _BuildSymbolTable(self, tokens):
        if len(self._errors) != 0:
            return
        constants = list(filter(lambda x: x.type is Lexer.kConstant, tokens))
        identifiers = list(filter(lambda x: x.type is Lexer.kIdentifier, tokens))
        return SymbolTable(constants, identifiers)

    def _BuildProgramInternalForm(self, tokens):
        if len(self._errors) != 0:
            return
        return ProgramInternalForm(tokens, self._st)


class SymbolTable:
    def __init__(self, constants, identifiers):
        self.const_to_code = {}
        self.code_to_const = {}
        self.id_to_code = {}
        self.code_to_id = {}
        num_constants = 0
        for constant in constants:
            if constant.content not in self.const_to_code:
                self.const_to_code[constant.content] = num_constants
                self.code_to_const[num_constants] = constant.content
                num_constants += 1
        num_identifiers = 0
        for identifier in identifiers:
            if identifier.content not in self.id_to_code:
                self.code_to_id[num_identifiers] = identifier.content
                self.id_to_code[identifier.content] = num_identifiers
                num_identifiers += 1

    def __repr__(self):
        output = ""
        output += "Symbol Table :: Constants\n"
        for code, const in self.code_to_const.items():
            output += "{2} :: {1}\n".format(code, const, hash(const))
        output += '\n'
        output += "Symbol Table :: Identifiers\n"
        for code, id in self.code_to_id.items():
            output += "{2} :: {1}\n".format(code, id, hash(id))
        return output


class ProgramInternalForm:
    kMapping = {}
    all_tokens = [Lexer.kConstant, Lexer.kIdentifier]
    all_tokens += Lexer.kReservedList + Lexer.kSeparatorList + Lexer.kOperatorList
    for token in all_tokens:
        kMapping[token] = len(kMapping)


    def __init__(self, tokens, symbol_table):
        self._pif = []
        kMapping = ProgramInternalForm.kMapping
        for token in tokens:
            if token.type is Lexer.kConstant:
                self._pif.append((kMapping[Lexer.kConstant], \
                        hash(token.content)))
                        #symbol_table.const_to_code[token.content]))
            elif token.type is Lexer.kIdentifier:
                self._pif.append((kMapping[Lexer.kIdentifier], \
                        hash(token.content)))
                        #symbol_table.id_to_code[token.content]))
            else:
                self._pif.append((kMapping[token.content], -1))


    def __repr__(self):
        output = ""
        output += "Program Internal Form\n"
        for item in self._pif:
            output += repr(item) + '\n'
        return output
