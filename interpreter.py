# interpreter.py

from lexer import INTEGER, PLUS, MINUS, ASTERISK, SLASH, EOF


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(
                f"構文エラー: 期待していたトークンは {token_type}, 実際は {self.current_token.type}"
            )


    def factor(self):
        """factor : INTEGER"""
        # 現状、因子は整数のみ
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def term(self):
        """term : factor ((ASTERISK | SLASH) factor)*"""
        # 最初のfactorを取得
        result = self.factor()

        # '*' か '/' が続く限り、計算を続ける
        while self.current_token.type in (ASTERISK, SLASH):
            op = self.current_token
            if op.type == ASTERISK:
                self.eat(ASTERISK)
                result = result * self.factor()
            elif op.type == SLASH:
                self.eat(SLASH)
                # ゼロ除算のエラーチェック
                divisor = self.factor()
                if divisor == 0:
                    raise Exception("エラー: 0で割ることはできません")
                result = result / divisor

        return result

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        # 最初のtermを取得
        result = self.term()

        # '+' か '-' が続く限り、計算を続ける
        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif op.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result
