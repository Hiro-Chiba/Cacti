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
    LPAREN,
    RPAREN,
    EOF,
    IF,
    THEN,
    PRINT,
    EQ,
    NE,
    LT,
    GT,
    LTE,
    GTE,
)


class Interpreter:
    def __init__(self, lexer, symbol_table=None):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        # 外部から渡されたsymbol_tableがあればそれを使う（記憶の引き継ぎ）
        self.symbol_table = symbol_table if symbol_table is not None else {}

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(
                f"構文エラー: 期待していたトークンは {token_type}, 実際は {self.current_token.type}"
            )

    def program(self):
        """プログラム全体の入口"""
        return self.statement_list()

    def statement_list(self):
        """文リストの解析: statement (SEMI statement)*"""
        # 最初の文を解析
        results = [self.statement()]

        # セミコロンが続く限り、次の文を解析
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        # 対話モードのために最後の結果を返す
        return results[-1] if results else None

    def statement(self):
        """文の解析（司令塔）"""
        if self.current_token.type == LOOP:
            return self.loop_statement()
        elif self.current_token.type == IF:
            return self.if_statement()
        elif self.current_token.type == PRINT:
            return self.print_statement()
        elif self.current_token.type == ID and self.lexer.peek() == "=":
            return self.assignment_statement()
        else:
            return self.comparison()

    def print_statement(self):
        """print文の解析: PRINT expr"""
        self.eat(PRINT)
        # PRINTの後ろの式を評価
        value = self.expr()
        # 評価結果をコンソールに出力
        print(value)
        # print文は値を返さない
        return None


    def loop_statement(self):
        """loop文の解析"""
        self.eat(LOOP)
        # 'loop i from 1 to 5' 形式
        if self.current_token.type == ID:
            var_name = self.current_token.value
            self.eat(ID)
            self.eat(FROM)
            start_val = self.expr()
            self.eat(TO)
            end_val = self.expr()
            block_code = self.block()  # ブロックの中身を文字列として取得
            # ループ実行
            for i in range(int(start_val), int(end_val) + 1):
                self.symbol_table[var_name] = i  # ループ変数を更新
                # ブロックコードから新しいInterpreterを作って実行
                sub_interpreter = Interpreter(Lexer(block_code), self.symbol_table)
                sub_interpreter.program()
                self.symbol_table.update(sub_interpreter.symbol_table)
        # 'loop 5 times' 形式
        else:
            times = self.expr()
            self.eat(TIMES)
            block_code = self.block()
            # ループ実行
            for _ in range(int(times)):
                sub_interpreter = Interpreter(Lexer(block_code), self.symbol_table)
                sub_interpreter.program()
                self.symbol_table.update(sub_interpreter.symbol_table)
        return None  # ループ文は値を返さない

    def block(self):
        """ブロックの解析: { statement_list } を文字列として切り出す"""
        self.eat(LBRACE)  # Consume '{'

        # ブロック内の最初のトークンの開始位置を取得
        start_pos = self.lexer.token_start_pos

        nesting_level = 1
        while nesting_level > 0:
            if self.current_token.type == EOF:
                raise Exception("構文エラー: ブロックが閉じられていません")

            if self.current_token.type == LBRACE:
                nesting_level += 1
            elif self.current_token.type == RBRACE:
                nesting_level -= 1

            # マッチする閉じ括弧を見つけたらループを抜ける
            if nesting_level == 0:
                # この閉じ括弧の開始位置がブロックの終了位置
                end_pos = self.lexer.token_start_pos
                break

            self.eat(self.current_token.type)

        # テキストからブロックのコードを切り出す
        block_code = self.lexer.text[start_pos:end_pos]

        self.eat(RBRACE)  # 最後の '}' を消費

        return block_code

    def if_statement(self):
        """if文の解析: IF comparison THEN block"""
        self.eat(IF)
        condition = self.comparison()
        self.eat(THEN)

        block_code = self.block()  # ブロックの中身を文字列として取得

        if condition:
            # 条件がTrueなら、ブロックコードから新しいInterpreterを作って実行
            sub_interpreter = Interpreter(Lexer(block_code), self.symbol_table)
            sub_interpreter.program()
            self.symbol_table.update(sub_interpreter.symbol_table)

        return None  # if文は値を返さない

    def comparison(self):
        """比較式の解析: expr (comp_op expr)?"""
        result = self.expr()

        op_types = (EQ, NE, LT, GT, LTE, GTE)
        if self.current_token.type in op_types:
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
        """factor : INTEGER | STRING | LPAREN expr RPAREN | ID"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == STRING:  # このelifを追加
            self.eat(STRING)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        elif token.type == ID:
            self.eat(ID)
            var_name = token.value
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
