# main.py

from lexer import Lexer
from interpreter import Interpreter


def main():
    # グローバルなシンボルテーブル（記憶領域）を用意
    global_symbol_table = {}

    while True:
        try:
            text = input("Cacti > ")
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        # 実行のたびに、グローバルな記憶領域を渡してあげる
        interpreter = Interpreter(lexer, global_symbol_table)

        try:
            result = interpreter.program()
            if result is not None:
                print(result)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
