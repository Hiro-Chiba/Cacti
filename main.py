# main.py

from lexer import Lexer, Token, EOF


def main():
    input_text = " a = 10 * (5 + b) "
    lexer = Lexer(input_text)

    token = lexer.get_next_token()
    while token.type != EOF:
        print(token)
        token = lexer.get_next_token()

    print(token)


if __name__ == "__main__":
    main()
