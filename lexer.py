# lexer.py

# --- トークンの種類を定義 ---
# 予約語
LOOP, TIMES, FROM, TO = "LOOP", "TIMES", "FROM", "TO"
IF, THEN, ELSE = "IF", "THEN", "ELSE"
PRINT = "PRINT"

# ブロックと文の区切り
LBRACE, RBRACE, SEMI = "LBRACE", "RBRACE", "SEMI"

# 演算子・終端
ASSIGN, ID = "ASSIGN", "ID"
INTEGER, PLUS, MINUS, ASTERISK, SLASH, IDIV, LPAREN, RPAREN, EOF = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "ASTERISK",
    "SLASH",
    "IDIV",  # 整数除算 //
    "LPAREN",
    "RPAREN",
    "EOF",
)
STRING = "STRING"

# 比較演算子
EQ, NE, LT, GT, LTE, GTE = "EQ", "NE", "LT", "GT", "LTE", "GTE"


# --- トークンを表現するクラス ---
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

    __repr__ = __str__


# 予約語テーブル
RESERVED_KEYWORDS = {
    "loop": Token(LOOP, "loop"),
    "times": Token(TIMES, "times"),
    "from": Token(FROM, "from"),
    "to": Token(TO, "to"),
    "if": Token(IF, "if"),
    "then": Token(THEN, "then"),
    "else": Token(ELSE, "else"),
    "print": Token(PRINT, "print"),
}


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.token_start_pos = 0  # 例外時に位置のヒントを出すため

    # --- 低レベル移動 ---
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        return self.text[peek_pos]

    # --- ユーティリティ ---
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_line_comment(self):
        # 現在位置は '#' の直後を想定
        while self.current_char is not None and self.current_char != "\n":
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def string(self):
        # 先頭の " は呼び出し側で確認済み
        result = ""
        self.advance()  # 開始の " をスキップ
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char != '"':
            raise Exception("字句エラー: 文字列が閉じられていません")
        self.advance()  # 終了の " をスキップ
        return result

    def _id(self):
        # 先頭: 英字またはアンダースコア
        result = ""
        if self.current_char is not None and (
            self.current_char.isalpha() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()
        else:
            raise Exception("字句エラー: 不正な識別子の開始文字")

        # 続き: 英数字またはアンダースコア
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()

        return RESERVED_KEYWORDS.get(result.lower(), Token(ID, result))

    # --- メイン: 次トークンを返す ---
    def get_next_token(self):
        while self.current_char is not None:
            self.token_start_pos = self.pos

            # 空白スキップ
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # 行コメント（# 〜 改行）
            if self.current_char == "#":
                self.advance()
                self.skip_line_comment()
                continue

            # 予約語/識別子
            if self.current_char.isalpha() or self.current_char == "_":
                return self._id()

            # 整数
            if self.current_char.isdigit():
                value = self.integer()
                return Token(INTEGER, value)

            # 文字列
            if self.current_char == '"':
                return Token(STRING, self.string())

            # 括弧・ブロック・区切り
            if self.current_char == "{":
                self.advance()
                return Token(LBRACE, "{")
            if self.current_char == "}":
                self.advance()
                return Token(RBRACE, "}")
            if self.current_char == ";":
                self.advance()
                return Token(SEMI, ";")
            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")
            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            # 比較演算子（2文字優先）
            if self.current_char == "=" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(EQ, "==")
            if self.current_char == "!" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(NE, "!=")
            if self.current_char == "<" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(LTE, "<=")
            if self.current_char == ">" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(GTE, ">=")

            # 単文字の比較
            if self.current_char == "<":
                self.advance()
                return Token(LT, "<")
            if self.current_char == ">":
                self.advance()
                return Token(GT, ">")

            # 代入
            if self.current_char == "=":
                self.advance()
                return Token(ASSIGN, "=")

            # 算術
            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")
            if self.current_char == "*":
                self.advance()
                return Token(ASTERISK, "*")
            # 整数除算 //（2文字優先）
            if self.current_char == "/" and self.peek() == "/":
                self.advance()
                self.advance()
                return Token(IDIV, "//")
            if self.current_char == "/":
                self.advance()
                return Token(SLASH, "/")

            raise Exception(
                f"字句エラー: 不正な文字 '{self.current_char}' @pos={self.pos}"
            )

        return Token(EOF, None)
