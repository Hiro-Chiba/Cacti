# main.py

from lexer import Lexer
from interpreter import Interpreter


def main():
    # Interpreterを一度だけ作成し、記憶を保持させる
    lexer = Lexer("")
    interpreter = Interpreter(lexer)

    while True:
        try:
            text = input("Cacti > ")
        except EOFError:
            break
        if not text:
            continue

        # 新しい入力でLexerとInterpreterをリセット
        lexer = Lexer(text)
        interpreter.lexer = lexer
        interpreter.current_token = interpreter.lexer.get_next_token()

        # プログラムを実行
        result = interpreter.program()
        if result is not None:
            print(result)


if __name__ == "__main__":
    main()
