# interpreter.py

from lexer import (
    Lexer,
    Token,
    STRING,
    LOOP,
    TIMES,
    FROM,
    TO,
    LBRACE,
    RBRACE,
    SEMI,
    ID,
    ASSIGN,
    INTEGER,
    PLUS,
    MINUS,
    ASTERISK,
    SLASH,
    IDIV,
    LPAREN,
    RPAREN,
    EOF,
    IF,
    THEN,
    ELSE,
    PRINT,
    EQ,
    NE,
    LT,
    GT,
    LTE,
    GTE,
)


class Interpreter:
    def __init__(self, lexer: Lexer, symbol_table=None):
        self.lexer = lexer
        # 1トークン先読み体制
        self.current_token = self.lexer.get_next_token()
        self.next_token = self.lexer.get_next_token()
        # 外部から渡された symbol_table があれば引き継ぐ
        self.symbol_table = symbol_table if symbol_table is not None else {}

    # トークン前進（current <- next, next <- next_next）
    def _advance(self):
        self.current_token = self.next_token
        self.next_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self._advance()
        else:
            raise Exception(
                f"構文エラー: 期待していたトークンは {token_type}, 実際は {self.current_token.type} @pos={self.lexer.token_start_pos}"
            )

    # エントリポイント
    def program(self):
        return self.statement_list()

    def statement_list(self):
        results = [self.statement()]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            # 末尾セミコロン許容（; EOF）のため、EOF なら抜ける
            if self.current_token.type == EOF:
                break
            results.append(self.statement())
        return results[-1] if results else None

    def statement(self):
        if self.current_token.type == LOOP:
            return self.loop_statement()
        elif self.current_token.type == IF:
            return self.if_statement()
        elif self.current_token.type == PRINT:
            return self.print_statement()
        elif self.current_token.type == ID and self.next_token.type == ASSIGN:
            return self.assignment_statement()
        else:
            return self.comparison()

    def print_statement(self):
        self.eat(PRINT)
        value = self.expr()
        print(value)
        return None

    def loop_statement(self):
        """loop i from A to B { ... } / loop N times { ... }"""
        self.eat(LOOP)
        # 形式1: loop i from A to B
        if self.current_token.type == ID:
            var_name = self.current_token.value
            self.eat(ID)
            self.eat(FROM)
            start_val = int(self.expr())
            self.eat(TO)
            end_val = int(self.expr())
            block_code = self.block()

            step = 1 if start_val <= end_val else -1
            for i in range(start_val, end_val + step, step):
                self.symbol_table[var_name] = i
                sub_interpreter = Interpreter(Lexer(block_code), self.symbol_table)
                sub_interpreter.program()
        # 形式2: loop N times
        else:
            times = int(self.expr())
            self.eat(TIMES)
            block_code = self.block()
            for _ in range(times):
                sub_interpreter = Interpreter(Lexer(block_code), self.symbol_table)
                sub_interpreter.program()
        return None

    def block(self):
        """{ statement_list } をテキストから丸ごと切り出して返す"""
        self.eat(LBRACE)
        start_pos = self.lexer.token_start_pos  # 最初の中身の開始位置
        nesting = 1
        while nesting > 0:
            if self.current_token.type == EOF:
                raise Exception("構文エラー: ブロックが閉じられていません")
            if self.current_token.type == LBRACE:
                nesting += 1
            elif self.current_token.type == RBRACE:
                nesting -= 1
                if nesting == 0:
                    end_pos = self.lexer.token_start_pos
                    break
            # 次のトークンへ
            self._advance()

        block_code = self.lexer.text[start_pos:end_pos]
        self.eat(RBRACE)  # '}' を消費
        return block_code

    def if_statement(self):
        """if comparison then block (else block)?"""
        self.eat(IF)
        condition = self.comparison()
        self.eat(THEN)
        then_block = self.block()
        else_block = None
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            else_block = self.block()

        if condition:
            sub = Interpreter(Lexer(then_block), self.symbol_table)
            sub.program()
        elif else_block is not None:
            sub = Interpreter(Lexer(else_block), self.symbol_table)
            sub.program()
        return None

    # 比較: expr (op expr)?
    def comparison(self):
        result = self.expr()
        if self.current_token.type in (EQ, NE, LT, GT, LTE, GTE):
            op = self.current_token
            self.eat(op.type)
            right = self.expr()
            if op.type == EQ:
                return result == right
            if op.type == NE:
                return result != right
            if op.type == LT:
                return result < right
            if op.type == GT:
                return result > right
            if op.type == LTE:
                return result <= right
            if op.type == GTE:
                return result >= right
        return result

    def assignment_statement(self):
        # 左辺
        variable = self.current_token
        self.eat(ID)
        # '='
        self.eat(ASSIGN)
        # 右辺
        value = self.expr()
        self.symbol_table[variable.value] = value
        return None

    # --- 式パーサ ---
    def factor(self):
        """factor : ('+'|'-') factor | INTEGER | STRING | LPAREN expr RPAREN | ID"""
        token = self.current_token

        # 単項演算子
        if token.type == PLUS:
            self.eat(PLUS)
            return +self.factor()
        if token.type == MINUS:
            self.eat(MINUS)
            return -self.factor()

        if token.type == INTEGER:
            val = token.value
            self.eat(INTEGER)
            return val
        elif token.type == STRING:
            val = token.value
            self.eat(STRING)
            return val
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        elif token.type == ID:
            name = token.value
            self.eat(ID)
            if name not in self.symbol_table:
                raise NameError(f"エラー: 変数 '{name}' は定義されていません")
            return self.symbol_table[name]
        else:
            raise Exception(
                f"構文エラー: 不正な因子 {token.type} @pos={self.lexer.token_start_pos}"
            )

    def term(self):
        """term : factor (('*' | '/' | '//') factor)*"""
        result = self.factor()
        while self.current_token.type in (ASTERISK, SLASH, IDIV):
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
            elif op.type == IDIV:
                self.eat(IDIV)
                divisor = self.factor()
                if divisor == 0:
                    raise Exception("エラー: 0で割ることはできません")
                result = result // divisor
        return result

    def _safe_add(self, a, b):
        # 文字列同士/数値同士のみ許可
        if isinstance(a, str) and isinstance(b, str):
            return a + b
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a + b
        raise TypeError(
            "エラー: 文字列と数値の加算はできません（明示的に str() などで変換してください）"
        )

    def expr(self):
        """expr : term (('+' | '-') term)*"""
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
                result = self._safe_add(result, self.term())
            elif op.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()
        return result
