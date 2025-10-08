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
        """ポインタを一つ進めて、current_charを更新する"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # 文字列の終端
        else:
            self.current_char = self.text[self.pos]

    def get_next_token(self):
        """textの中から次のトークンを見つけて返す"""
        while self.current_char is not None:
            if self.current_char.isspace():
                # 現在の文字が空白の場合、スキップする
                self.advance()
                continue

            if self.current_char == "+":
                # '+' を見つけたら、PLUSトークンを生成して返す
                token = Token(PLUS, self.current_char)
                self.advance()
                return token

            if self.current_char == "-":
                # '-' を見つけたら、MINUSトークンを生成して返す
                token = Token(MINUS, self.current_char)
                self.advance()
                return token

            if self.current_char == "*":
                # '*' を見つけたら、ASTERISKトークンを生成して返す
                token = Token(ASTERISK, self.current_char)
                self.advance()
                return token

            if self.current_char == "/":
                # '/' を見つけたら、SLASHトークンを生成して返す
                token = Token(SLASH, self.current_char)
                self.advance()
                return token

            # 上のどの条件にも当てはまらない文字が見つかった場合
            raise Exception(f"不正な文字です: '{self.current_char}'")

        # ループが終了した場合（文字列の最後まで読み終わった場合）
        return Token(EOF, None)