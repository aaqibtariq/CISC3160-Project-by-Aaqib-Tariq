import Token
class CheckNode(object):
    def check(self, node):
        method_name = 'check_' + type(node).__name__
        checker = getattr(self, method_name, self.generic_check)
        return checker(node)

    def generic_check(self, node):
        raise Exception('No check_{} method'.format(type(node).__name__))


class Interpreter(CheckNode):

    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def check_BinOp(self, node):
        if node.op.type == Token.PLUS:
            return self.check(node.left) + self.check(node.right)
        elif node.op.type == Token.MINUS:
            return self.check(node.left) - self.check(node.right)
        elif node.op.type == Token.MUL:
            return self.check(node.left) * self.check(node.right)
        elif node.op.type == Token.ID:
            return self.check(node.left) // self.check(node.right)

    def check_Num(self, node):
        return node.value

    def check_UnaryOp(self, node):
        op = node.op.type
        if op == Token.PLUS:
            return +self.check(node.expr)
        elif op == Token.MINUS:
            return -self.check(node.expr)

    def check_Compound(self, node):
        for child in node.children:
            self.check(child)

    def check_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.check(node.right)

    def check_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def check_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.check(tree)
