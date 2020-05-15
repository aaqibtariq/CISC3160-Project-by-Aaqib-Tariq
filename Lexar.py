# Lexical Analysis is the first phase of compiler also known as scanner. It converts the High level input program
# into a sequence of Tokens.

import Token
import re
class Lexer(object):
    def __init__(self, text):

        self.text = text

        self.pos = 0
        self.curr_char = self.text[self.pos]

    def error(self):
        raise Exception('Error')

    def skip_whitespace(self):
        while self.curr_char is not None and self.curr_char.isspace():
            self.advance()

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]



    def advance(self):

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]



    def _id(self):

        result = ''
        while self.curr_char is not None and self.curr_char.isalnum() or self.curr_char == '_':
            result += self.curr_char
            self.advance()

        token = Token.Token(Token.ID, result)
        return token

    def integer(self):

        literal = re.compile(r'(0){1}|([1-9])\d*')
        result = ''
        while self.curr_char is not None and self.curr_char.isdigit():
            result += self.curr_char
            self.advance()
        if literal.fullmatch(result) is not None:
            return int(result)
        else:
            self.error()

    def get_next_token(self):

        while self.curr_char is not None:

            if self.curr_char.isspace():
                self.skip_whitespace()
                continue

            if self.curr_char.isalpha():
                return self._id()

            if self.curr_char.isdigit():
                return Token.Token(Token.INTEGER, self.integer())

            if self.curr_char == '=':
                self.advance()
                return Token.Token(Token.ASSIGN, '=')

            if self.curr_char == ';':
                self.advance()
                return Token.Token(Token.SEMI, ';')

            if self.curr_char == '+':
                self.advance()
                return Token.Token(Token.PLUS, '+')

            if self.curr_char == '-':
                self.advance()
                return Token.Token(Token.MINUS, '-')

            if self.curr_char == '*':
                self.advance()
                return Token.Token(Token.MUL, '*')

            if self.curr_char == '(':
                self.advance()
                return Token.Token(Token.LPAREN, '(')

            if self.curr_char == ')':
                self.advance()
                return Token.Token(Token.RPAREN, ')')

            self.error()

        return Token.Token(Token.EOF, None)
