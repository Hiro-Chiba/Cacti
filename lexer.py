# lexer.py

# --- トークンの種類を定義 ---
ASSIGN, ID = "ASSIGN", "ID"
INTEGER, PLUS, MINUS, ASTERISK, SLASH, LPAREN, RPAREN, EOF = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "ASTERISK",
    "SLASH",
    "LPAREN",
    "RPAREN",
    "EOF",
)


# --- トークンを表現するクラス ---
class Token:
    def __init__(self, type, value):
        self.type = type  # トークンの種類 (INTEGER, PLUSなど)
        self.value = value  # トークンの値 (10, '+'など)

    def __str__(self):
        # print(token) とした時に見やすくするメソッド
        return f"Token({self.type}, {repr(self.value)})"


# --- Lexer本体のクラス ---
# lexer.py の Lexer クラス部分


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        # (このメソッドは変更なし)
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def integer(self):
        """複数桁の整数を読み進めて、その数値を返す"""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        """英数字からなる識別子を読み取る"""
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        return Token(ID, result)

    def get_next_token(self):
        """textの中から次のトークンを見つけて返す"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue

            if self.current_char.isalpha():
                # 文字で始まる場合は変数名とみなす
                return self._id()

            if self.current_char.isdigit():
                # 数字を見つけたら、integer()メソッドを呼び出す
                value = self.integer()
                return Token(INTEGER, value)

            if self.current_char == "=":
                # '=' は代入演算子とみなす
                token = Token(ASSIGN, self.current_char)
                self.advance()
                return token

            if self.current_char == "(":
                token = Token(LPAREN, self.current_char)
                self.advance()
                return token

            if self.current_char == ")":
                token = Token(RPAREN, self.current_char)
                self.advance()
                return token

            if self.current_char == "+":
                token = Token(PLUS, self.current_char)
                self.advance()
                return token

            if self.current_char == "-":
                token = Token(MINUS, self.current_char)
                self.advance()
                return token

            if self.current_char == "*":
                token = Token(ASTERISK, self.current_char)
                self.advance()
                return token

            if self.current_char == "/":
                token = Token(SLASH, self.current_char)
                self.advance()
                return token

            raise Exception(f"不正な文字です: '{self.current_char}'")

        return Token(EOF, None)
