# interpreter.py

from lexer import INTEGER, PLUS, MINUS, ASTERISK, SLASH, EOF


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        # 最初のトークンを取得してセットする
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        """
        現在のトークンが期待する型(token_type)と一致すれば、
        トークンを「消費」して、次のトークンに進める。
        一致しなければエラーを発生させる。
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(
                f"構文エラー: 期待していたトークンは {token_type}, 実際は {self.current_token.type}"
            )

    def expr(self):
        """
        式の解析と評価を行う
        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER ...
        """
        # 最初のトークンは必ず数字であるはず
        result = self.current_token.value
        self.eat(INTEGER)

        while self.current_token.type in (PLUS, MINUS, ASTERISK, SLASH):
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
                result = result + self.current_token.value
                self.eat(INTEGER)
            elif op.type == MINUS:
                self.eat(MINUS)
                result = result - self.current_token.value
                self.eat(INTEGER)
            elif op.type == ASTERISK:
                self.eat(ASTERISK)
                result = result * self.current_token.value
                self.eat(INTEGER)
            elif op.type == SLASH:
                self.eat(SLASH)
                result = result / self.current_token.value
                self.eat(INTEGER)

        return result
