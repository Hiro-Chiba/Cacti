# main.py

from lexer import Lexer, Token, EOF


def main():
    input_text = " + - * / "
    lexer = Lexer(input_text)

    # get_next_token() を呼び続けて、EOFトークンが出るまで繰り返す
    token = lexer.get_next_token()
    while token.type != EOF:
        print(token)
        token = lexer.get_next_token()

    # 最後にEOFトークンも表示してみる
    print(token)


if __name__ == "__main__":
    main()
