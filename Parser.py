# Parser is that phase of compiler which takes token string as input and with the help of existing grammar,
# converts it into the corresponding parse tree. Parser is also known as Syntax Analyzer

import Token
class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Assign(AST):
    def __init__(self, left, op, right,semi):
        self.left = left
        self.token = self.op = op
        self.right = right
        self.semi = semi


class Var(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer

        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def take(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()


    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.take(Token.ASSIGN)
        right = self.expr()
        semi = self.current_token
        self.take(Token.SEMI)
        node = Assign(left, token, right,semi)
        return node


    def program(self):
        node = self.assignment_statement()
        while self.current_token.type in (Token.ASSIGN):
            token = self.current_token
            if(token.type == Token.ASSIGN):
                self.take(Token.DOT)

            node = BinOp(left=node, op=token, right=self.assignment_statement())

        return node



    def variable(self):
        node = Var(self.current_token)
        self.take(Token.ID)
        return node

    def empty(self):
        return NoOp()

    def expr(self):

        node = self.term()

        while self.current_token.type in (Token.PLUS, Token.MINUS):
            token = self.current_token
            if token.type == Token.PLUS:
                self.take(Token.PLUS)
            elif token.type == Token.MINUS:
                self.take(Token.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node



    def term(self):

        node = self.factor()

        while self.current_token.type in (Token.MUL):
            token = self.current_token
            if token.type == Token.MUL:
                self.take(Token.MUL)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        token = self.current_token
        if token.type == Token.PLUS:
            self.take(Token.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == Token.MINUS:
            self.take(Token.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == Token.INTEGER:
            self.take(Token.INTEGER)
            return Num(token)
        elif token.type == Token.LPAREN:
            self.take(Token.LPAREN)
            node = self.expr()
            self.take(Token.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def parse(self):
        node = self.program()
        if self.current_token.type != Token.EOF:
            self.error()

        return node

