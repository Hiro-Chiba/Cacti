# main.py

from lexer import Lexer, Token, EOF

def main():
    # テストする文字列を数字入りのものに変更
    input_text = "  123 + 50 * 2 - 8 / 4  "
    lexer = Lexer(input_text)

    # (ここから下のロジックは変更なし)
    token = lexer.get_next_token()
    while token.type != EOF:
        print(token)
        token = lexer.get_next_token()
    
    print(token)

if __name__ == '__main__':
    main()