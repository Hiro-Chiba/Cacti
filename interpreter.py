# interpreter.py

from lexer import ID, ASSIGN, INTEGER, PLUS, MINUS, ASTERISK, SLASH, LPAREN, RPAREN, EOF


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.symbol_table = {}

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(
                f"構文エラー: 期待していたトークンは {token_type}, 実際は {self.current_token.type}"
            )

    def program(self):
        """プログラム全体の入口"""
        # 文の解析と実行
        return self.statement()

    def statement(self):
        """文の解析"""
        if self.current_token.type == ID:
            # 次のトークンを覗き見して '=' かどうかを判断
            if self.lexer.peek().type == ASSIGN:
                return self.assignment_statement()
            else:
                return self.expr()
        else:
            return self.expr()

    def assignment_statement(self):
        """代入文の解析: ID ASSIGN expr"""
        # 変数名を取得
        variable = self.current_token
        self.eat(ID)

        # '=' を消費
        self.eat(ASSIGN)

        # 右辺の式を評価
        value = self.expr()

        # シンボルテーブルに変数を保存
        self.symbol_table[variable.value] = value
        # 代入文は値を返さない（Noneを返す）
        return None

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN | ID"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        elif token.type == ID:
            self.eat(ID)
            var_name = token.value
            # シンボルテーブルから値を取得
            value = self.symbol_table.get(var_name)
            if value is None:
                raise NameError(f"エラー: 変数 '{var_name}' は定義されていません")
            else:
                return value

    def term(self):
        result = self.factor()
        while self.current_token.type in (ASTERISK, SLASH):
            op = self.current_token
            if op.type == ASTERISK:
                self.eat(ASTERISK)
                result = result * self.factor()
            elif op.type == SLASH:
                self.eat(SLASH)
                divisor = self.factor()
                if divisor == 0:
                    raise Exception("エラー: 0で割ることはできません")
                result = result / divisor
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif op.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()
        return result
