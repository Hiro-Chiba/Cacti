# main.py

from lexer import Lexer, Token, EOF

def main():
    input_text = """
    loop i from 1 to 5 {
        a = a + i;
    }
    loop 3 times {
        b = "hello";
    }
    """
    lexer = Lexer(input_text)

    token = lexer.get_next_token()
    while token.type != EOF:
        print(token)
        token = lexer.get_next_token()
    
    print(token)

if __name__ == '__main__':
    main()