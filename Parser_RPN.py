from Lexer import Lexer
from Token import Token, TokenType
from typing import Callable

from AST import Node, NodeType
from AST import Statement, Expression, Program
from AST import ExpressionStatement, LetStatement, FunctionStatement, BlockStatement, ReturnStatement, AssignStatement, IfStatement, WhileStatement, ImportStatement
from AST import InfixExpression, CallExpression, StringExpression, SuffixExpression
from AST import IntegerLiteral, FloatLiteral, IdentifierLiteral, BooleanLiteral, StringLiteral
from AST import FunctionParameter

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer

        self.errors: list[str] = []
        
        self.current_token: Token = None
        self.peek_token: Token = None

        self.value_parse_fns: dict[TokenType, Callable] = {
            TokenType.INT: self.__parse_int_literal,
            TokenType.FLOAT: self.__parse_float_literal,
            TokenType.IDENT: self.__parse_identifier,
            
            TokenType.TRUE: self.__parse_boolean,
            TokenType.FALSE: self.__parse_boolean,
            
            TokenType.STRINGSTART: self.__parse_string_expression,
        }
        self.operator_parse_fns: dict[TokenType, Callable] = {
            TokenType.ADD: self.__parse_infix_expression,
            TokenType.SUB: self.__parse_infix_expression,
            TokenType.MUL: self.__parse_infix_expression,
            TokenType.DIV: self.__parse_infix_expression,
            
            TokenType.MORE: self.__parse_infix_expression,
            TokenType.LESS: self.__parse_infix_expression,
            TokenType.EQLS: self.__parse_infix_expression,
            
        }
        self.modifier_parse_fns: dict[TokenType, Callable] = {
            TokenType.NOT: self.__parse_suffix_expression,
            TokenType.NEGATIVE: self.__parse_suffix_expression,
            TokenType.LBRACKET: self.__parse_call_expression
        }
        
        self.__next_token()
        self.__next_token()
        
    # region Parser Helpers
    def __next_token(self) -> None:
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()
        # print(f"New token: {self.current_token}")
        
    def __current_token_is(self, tt: TokenType) -> bool:
        return self.current_token.type == tt
        
    def __peek_token_is(self, tt: TokenType) -> bool:
        return self.peek_token.type == tt
    
    def __expect_peek(self, tt: TokenType) -> bool:
        if self.__peek_token_is(tt):
            self.__next_token()
            return True
        else:
            self.__peek_error(tt)
            return False
        
    def __peek_error(self, tt: TokenType) -> None:
        self.errors.append(f"Expected next token to be {tt}, got {self.peek_token.type} instead.")
        
    def __no_parse_fn_error(self, tt: TokenType):
        self.errors.append(f"No Parse Function for {tt} found.")
        
    # endregion

    def parse_program(self) -> None:
        program: Program = Program()
        
        while self.current_token.type != TokenType.EOF:
            stmt: Statement = self.__parse_statement()
            # print(stmt)
            if stmt is not None:
                program.statements.append(stmt)
                
            self.__next_token()
            
        return program
    
    # region Statement Methods
    def __parse_statement(self) -> Statement:
        if self.current_token.type == TokenType.IDENT and not self.__peek_token_is(TokenType.LBRACKET):
            
            # Check for keyword at end of expression
            self.lexer.pause_lexer()
            paused_token = self.current_token
            paused_peek_token = self.peek_token
            
            self.__parse_expression()
            ending_token = self.current_token
            # print(f"Search ending token is {ending_token}")
            
            self.current_token = paused_token
            self.peek_token = paused_peek_token
            self.lexer.reset_lexer()
            
            # ending_token now has the keyword at the end of the expression :nod:
            
            if ending_token.type == TokenType.IS:
                # This is an assignment expression
                return self.__parse_assignment_statement()
            elif ending_token.type == TokenType.WHEN:
                # IF statement or WHILE statement
                return self.__parse_if_while_statement()
        
        # Check for import keyword
        if self.current_token.type == TokenType.STRINGSTART:
            
            # Check for keyword at end of line
            self.lexer.pause_lexer()
            paused_token = self.current_token
            paused_peek_token = self.peek_token
            
            while not self.peek_token.type in [TokenType.NEWLINE, TokenType.EOF]:
                self.__next_token()
            ending_token = self.current_token
            # print(f"Search ending token is {ending_token}")
            
            self.current_token = paused_token
            self.peek_token = paused_peek_token
            self.lexer.reset_lexer()
            
            if ending_token.type == TokenType.IMPORT:
                return self.__parse_import_statement()
            
            # ending_token now has the keyword at the end of the expression :nod:
        
        match self.current_token.type:
            case TokenType.TYPE:
                # Let Statement
                return self.__parse_let_statement()
                
            case TokenType.FUNCTION:
                # fn int main[] (block) end
                return self.__parse_function_statement()
            
            case _:
                stmt = self.__parse_expression_statement()
                # print(f"Attempting an expression statement {self.current_token}")
            
        if self.current_token.type == TokenType.RETURN:
            stmt: ReturnStatement = ReturnStatement(return_value=stmt.expr)
            # Skip newline if exists
            if self.__peek_token_is(TokenType.NEWLINE):
                self.__next_token()
        
        return stmt
    
    def __parse_expression_statement(self) -> ExpressionStatement:
        stmt: ExpressionStatement = ExpressionStatement()
        stmt.expr = self.__parse_expression()
        return stmt
    
    def __parse_let_statement(self) -> LetStatement:
        stmt: LetStatement = LetStatement()
        # int a [expr] kig
        stmt.value_type = self.current_token.literal
        
        if not self.__expect_peek(TokenType.IDENT):
            return None
        
        stmt.name = self.__parse_identifier()
        self.__next_token()
        expr: Expression = self.__parse_expression()
        stmt.value = expr
        
        if not self.__current_token_is(TokenType.IS):
            return None
        
        # End with new line
        if not self.__expect_peek(TokenType.NEWLINE):
            return None
        
        return stmt
        
    def __parse_function_statement(self) -> FunctionStatement:
        stmt: FunctionStatement = FunctionStatement()
        # fn int main[] (block) end
        
        if not self.__expect_peek(TokenType.TYPE):
            return None
        
        stmt.return_type = self.current_token.literal
        
        if not self.__expect_peek(TokenType.IDENT):
            return None
        
        stmt.name = IdentifierLiteral(value=self.current_token.literal)
        
        if not self.__expect_peek(TokenType.LBRACKET):
            return None
        
        stmt.parameters = self.__parse_function_parameters()
        
        if not self.__expect_peek(TokenType.NEWLINE):
            return None
        # print(f"Function declare beginning, Should be of type Newline and is: {self.current_token.literal}")
        
        # Begin block
        
        stmt.body = self.__parse_block_statement()
        
        # End Block
        if not self.__current_token_is(TokenType.END):
            return None
        
        self.__next_token()
        if not self.__current_token_is(TokenType.NEWLINE) and not self.__current_token_is(TokenType.EOF):
            return None
        
        return stmt
    
    def __parse_function_parameters(self) -> list[FunctionParameter]:
        params: list[FunctionParameter] = []
        
        if self.__peek_token_is(TokenType.RBRACKET):
            self.__next_token()
            return params
        
        self.__next_token()
        
        # int 5
        
        if not self.__current_token_is(TokenType.TYPE):
            return None
        first_param: FunctionParameter = FunctionParameter(value_type=self.current_token.literal)
        
        if not self.__expect_peek(TokenType.IDENT):
            return None
        
        first_param.name = self.current_token.literal
        params.append(first_param)
        
        while self.__peek_token_is(TokenType.COMMA):
            self.__next_token()
            
            if not self.__expect_peek(TokenType.TYPE):
                return None
            param: FunctionParameter = FunctionParameter(value_type=self.current_token.literal)
            
            if not self.__expect_peek(TokenType.IDENT):
                return None
            
            param.name = self.current_token.literal
            params.append(param)
            
        if not self.__expect_peek(TokenType.RBRACKET):
            return None
        
        return params
    
    def __parse_block_statement(self) -> BlockStatement:
        block_stmt: BlockStatement = BlockStatement()
        
        self.__next_token()
        
        while not self.current_token.type in [TokenType.END, TokenType.EOF, TokenType.AGAIN, TokenType.ELSE]:
            # print(f"Statement in block begins with {self.current_token}")
            stmt: Statement = self.__parse_statement()
            if stmt is not None:
                block_stmt.statements.append(stmt)
            # print(f"Statement in block ends with {self.current_token}")
            self.__next_token()
        
        return block_stmt
    
    def __parse_assignment_statement(self) -> AssignStatement:
        stmt: AssignStatement = AssignStatement()
        
        # print(f"Assigning to {self.current_token.literal}")
        stmt.ident = IdentifierLiteral(value=self.current_token.literal)
        self.__next_token() # Move from initial Identifier
        stmt.right_value = self.__parse_expression()
        
        if not self.__current_token_is(TokenType.IS):
            return None
        
        if not self.__expect_peek(TokenType.NEWLINE):
            return None
        
        return stmt
    
    def __parse_if_while_statement(self) -> Statement:
        condition: Expression = None
        first_block: BlockStatement = None
        alternative: BlockStatement = None

        condition = self.__parse_expression()
        
        if not self.__current_token_is(TokenType.WHEN):
            return None
        # Current Token is WHEN
        if self.__peek_token_is(TokenType.NEWLINE):
            self.__next_token()
            # Skip newline
        
        first_block = self.__parse_block_statement()
        
        if self.__current_token_is(TokenType.AGAIN):
            # WHILE statement
            # Skip newline if exists
            if self.__peek_token_is(TokenType.NEWLINE):
                self.__next_token()
            return WhileStatement(condition=condition, body=first_block)
        else:
            # IF Statement
            if self.__current_token_is(TokenType.ELSE):
                # Skip newline if exists
                if self.__peek_token_is(TokenType.NEWLINE):
                    self.__next_token()
                alternative = self.__parse_block_statement()
                
            # Current token should be "END"
            # Skip newline if exists
            if self.__peek_token_is(TokenType.NEWLINE):
                self.__next_token()
            
            return IfStatement(condition, first_block, alternative)
    
    def __parse_import_statement(self) -> ImportStatement:
        # Expecting first token to be stringstart
        if not self.__current_token_is(TokenType.STRINGSTART):
            return None
        if not self.__expect_peek(TokenType.STRING):
            return None
        file_path: str = self.current_token.literal # Expects a string
        
        if not self.__expect_peek(TokenType.STRINGEND):
            return None
        if not self.__expect_peek(TokenType.IMPORT):
            return None
        
        stmt: ImportStatement = ImportStatement(file_path=file_path)
        if not self.__expect_peek(TokenType.NEWLINE):
            return None
        
        return stmt
    # endregion
    
    # region Expression Methods
    def __parse_expression(self) -> Expression:
        stack: list[Expression] = []
        
        # Parse current expression
        while self.current_token.type in self.value_parse_fns or self.current_token.type in self.operator_parse_fns or self.current_token.type in self.modifier_parse_fns:
            # Literals and values
            if self.current_token.type in self.value_parse_fns:
                # Push Literal onto Stack
                literal_fn: Callable | None = self.value_parse_fns.get(self.current_token.type)
                if literal_fn is None:
                    self.__no_parse_fn_error(self.current_token.type)
                    return None
                lit_expr: Expression = literal_fn()
                # print(lit_expr)
                
                stack.append(lit_expr)
                
            # Operators and methods
            elif self.current_token.type in self.operator_parse_fns:
                # Pop off last two Expressions and put the operator in
                operator_fn: Callable | None = self.operator_parse_fns.get(self.current_token.type)
                if operator_fn is None:
                    self.__no_parse_fn_error(self.current_token.type)
                    return None
                
                right_expr: Expression = stack.pop()
                left_expr: Expression = stack.pop()
                
                oper_expr: Expression = operator_fn(left_expr, right_expr)
                stack.append(oper_expr)
                
            # Modifiers
            elif self.current_token.type in self.modifier_parse_fns:
                # Pop off last expression and modify it, somehow
                modifier_fn: Callable | None = self.modifier_parse_fns.get(self.current_token.type)
                if modifier_fn is None:
                    self.__no_parse_fn_error(self.current_token.type)
                    return None
                
                left_expr: Expression = stack.pop()
                
                mod_expr: Expression = modifier_fn(left_expr)
                stack.append(mod_expr)
            
            # print("before", self.current_token)
            self.__next_token()
            # print("after", self.current_token)
        
        return stack[0] if stack else None
    
    def __parse_infix_expression(self, left_node: Expression, right_node: Expression) -> Expression:
        suffix_expr: InfixExpression = InfixExpression(left_node=left_node, operator=self.current_token.literal, right_node=right_node)
        
        return suffix_expr
    
    def __parse_call_expression(self, function: Expression) -> CallExpression:
        expr: CallExpression = CallExpression(function=function)
        expr.arguments = self.__parse_expression_list(TokenType.RBRACKET)
        
        # print(f"Call ends on {self.current_token.literal}")
        
        return expr
    
    def __parse_expression_list(self, end: TokenType) -> list[Expression]:
        e_list: list[Expression] = []
        
        if self.__peek_token_is(end):
            self.__next_token()
            return e_list
        
        self.__next_token()
        
        e_list.append(self.__parse_expression())
        
        while self.__current_token_is(TokenType.COMMA):
            # print(self.current_token)
            self.__next_token()
            
            e_list.append(self.__parse_expression())
            
        if not self.__current_token_is(end):
            return None
        
        return e_list
    
    def __parse_string_expression(self) -> StringExpression:
        expr: StringExpression = StringExpression()
        contents: list[Expression] = []
        # Consume <
        self.__next_token()
        
        while not self.__current_token_is(TokenType.STRINGEND):
            # print(f"Inside of a string: looking at {self.current_token}")
            if self.__current_token_is(TokenType.STRING):
                contents.append(self.__parse_string_literal())
                
            elif self.__current_token_is(TokenType.LPAREN):
                # Consume (
                self.__next_token()
                contents.append(self.__parse_expression())
                # Consume )
                if not self.__current_token_is(TokenType.RPAREN):
                    return None
            
            self.__next_token()
        
        # Consume >
        # self.__next_token()
        # for content in contents:
        #     print(content.json())
        expr.contents = contents
        # print(contents)
        return expr
    
    def __parse_suffix_expression(self, left_node: Expression) -> SuffixExpression:
        suffix_expr: SuffixExpression = SuffixExpression(operator=self.current_token.literal, left_node=left_node)
        
        return suffix_expr
    
    # endregion

    # region Prefix Methods
    def __parse_identifier(self) -> IdentifierLiteral:
        # int a
        iden_lit: IdentifierLiteral = IdentifierLiteral()
        
        iden_lit.value = self.current_token.literal
        
        return iden_lit
        
    def __parse_int_literal(self) -> Expression:
        int_lit: IntegerLiteral = IntegerLiteral()
        
        try:
            int_lit.value = int(self.current_token.literal)
        except:
            self.errors.append(f"Could not parse `{self.current_token.literal}` as an integer.")
            return None
        
        return int_lit
    
    def __parse_float_literal(self) -> Expression:
        float_lit: FloatLiteral = FloatLiteral()
        
        try:
            float_lit.value = float(self.current_token.literal)
        except:
            self.errors.append(f"Could not parse `{self.current_token.literal}` as a float.")
            return None
        
        return float_lit
    
    def __parse_boolean(self) -> BooleanLiteral:
        return BooleanLiteral(value=self.__current_token_is(TokenType.TRUE))
    
    def __parse_string_literal(self) -> StringLiteral:
        # print(f"Literal string: {self.current_token.literal}")
        return StringLiteral(value=self.current_token.literal)
    # endregion