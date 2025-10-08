# lexer.py

# --- トークンの種類を定義 ---
# 予約語
IF, THEN, END = "IF", "THEN", "END"

# 演算子
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
# 比較演算子
EQ, NE, LT, GT, LTE, GTE = "EQ", "NE", "LT", "GT", "LTE", "GTE"


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

RESERVED_KEYWORDS = {
    "if": Token(IF, "if"),
    "then": Token(THEN, "then"),
    "end": Token(END, "end"),
}


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
        """英数字からなる識別子（または予約語）を読み取る"""
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        # 読み取った単語が予約語なら予約語トークンを、そうでなければIDトークンを返す
        return RESERVED_KEYWORDS.get(result.lower(), Token(ID, result))

    def peek(self):
        """次のトークンを覗き見する"""
        # 現在の状態を保存
        original_pos = self.pos
        original_current_char = self.current_char

        # 次のトークンを取得
        token = self.get_next_token()

        # 状態を元に戻す
        self.pos = original_pos
        self.current_char = original_current_char

        return token

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

            if self.current_char == "=" and self.peek().value == "=":
                self.advance()
                self.advance()
                return Token(EQ, "==")

            if self.current_char == "!" and self.peek().value == "=":
                self.advance()
                self.advance()
                return Token(NE, "!=")

            if self.current_char == "<" and self.peek().value == "=":
                self.advance()
                self.advance()
                return Token(LTE, "<=")

            if self.current_char == ">" and self.peek().value == "=":
                self.advance()
                self.advance()
                return Token(GTE, ">=")

            if self.current_char == "<":
                self.advance()
                return Token(LT, "<")

            if self.current_char == ">":
                self.advance()
                return Token(GT, ">")

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
