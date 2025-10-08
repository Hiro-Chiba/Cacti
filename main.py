# main.py

from lexer import Lexer
from interpreter import Interpreter

def main():
    while True:
        try:
            # ターミナルから計算式を読み込む
            text = input('Cacti > ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()