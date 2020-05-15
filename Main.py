import Interpreter
import Parser
import Lexar

def main():
    while True:
        try:
            text = input('Input> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexar.Lexer(text)
        parser = Parser.Parser(lexer)
        interpreter = Interpreter.Interpreter(parser)
        result = interpreter.interpret()
        print("\nOutPut: ".join("{} = {}".format(a, b) for a, b in interpreter.GLOBAL_SCOPE.items()))



if __name__ == '__main__':
    main()
