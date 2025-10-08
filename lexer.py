# lexer.py

# --- トークンの種類を定義 ---
INTEGER, PLUS, MINUS, ASTERISK, SLASH, EOF = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "ASTERISK",
    "SLASH",
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

    # --- ▼▼▼ ここから追加・変更 ▼▼▼ ---

    def integer(self):
        """複数桁の整数を読み進めて、その数値を返す"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """textの中から次のトークンを見つけて返す"""
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.advance()
                continue
            
            # --- ここからが新しいロジック ---
            if self.current_char.isdigit():
                # 数字を見つけたら、integer()メソッドを呼び出す
                value = self.integer()
                return Token(INTEGER, value)
            # --- ここまでが新しいロジック ---

            if self.current_char == '+':
                token = Token(PLUS, self.current_char)
                self.advance()
                return token

            if self.current_char == '-':
                token = Token(MINUS, self.current_char)
                self.advance()
                return token

            if self.current_char == '*':
                token = Token(ASTERISK, self.current_char)
                self.advance()
                return token

            if self.current_char == '/':
                token = Token(SLASH, self.current_char)
                self.advance()
                return token

            raise Exception(f"不正な文字です: '{self.current_char}'")

        return Token(EOF, None)