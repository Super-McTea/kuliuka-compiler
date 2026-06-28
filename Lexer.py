from Token import Token, TokenType, lookup_ident
from typing import Any


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source

        self.position: int = -1
        self.read_position: int = 0
        self.line_no: int = 1
        
        self.current_char: str | None = None
        
        self.string_mode = False
        self.reading_string = False

        self.__read_char()
        
        self.pause = False
        
        self.last_was_newline = False
        
    def __read_char(self) -> None:
        if self.read_position >= len(self.source):
            self.current_char = None # EOF flag
        else:
            self.current_char = self.source[self.read_position]
            
        self.position = self.read_position
        self.read_position += 1
        
    def __peek_char(self) -> str | None:
        if self.read_position >= len(self.source):
            return None
        
        return self.source[self.read_position]
        
    def pause_lexer(self) -> None:
        self.paused_position = self.position
        self.paused_read_position = self.read_position
        self.paused_line_no = self.line_no
        
        self.paused_char = self.current_char
        
        self.paused_reading_string = self.reading_string
        self.paused_string_mode = self.string_mode
        
        self.pause = True
        
    def reset_lexer(self) -> None:
        self.position = self.paused_position
        self.read_position = self.paused_read_position
        self.line_no = self.paused_line_no
        
        self.current_char = self.paused_char
        
        self.reading_string = self.paused_reading_string
        self.string_mode = self.paused_string_mode
        
        self.pause = False
        
        
    def __skip_whitespace(self) -> None:
        while self.current_char in [' ', '\t'] or (self.last_was_newline and self.current_char in ['\n', '\r']):
            if self.current_char in ['\n', '\r']:
                self.line_no += 1
            
            self.__read_char()
        # print(f"Skipped whitespace to: {self.current_char}")
            
    def __new_token(self, tt: TokenType, literal: Any) -> Token:
        return Token(type=tt, literal=literal, line_no=self.line_no, position=self.position)
    
    def __is_letter(self, c: str) -> bool:
        return c.isalpha() or c == '_'
    
    def __read_number(self) -> Token:
        start_pos: int = self.position
        dot_count: int = 0;
        
        output: str = ""
        while self.current_char.isdigit() or self.current_char == '.':
            if self.current_char == '.':
                dot_count += 1
            
            if dot_count > 1:
                print(f"Too many decimals in number on line {self.line_no}, position {self.position}")
                return self.__new_token(TokenType.ILLEGAL, self.source[start_pos:self.position])
            
            output += self.source[self.position]
            self.__read_char()
            
            if self.current_char is None:
                break

        # clean up attached grammar characters
        if self.current_char in ['m', 'n', 'b', 'd', 'g']:
            self.__read_char()
            if self.current_char == 'g': # handle 'ng'
                self.__read_char()

        if dot_count == 0:
            return self.__new_token(TokenType.INT, int(output))
        else:
            return self.__new_token(TokenType.FLOAT, float(output))
        
    def __read_identifier(self) -> str:
        position = self.position
        while self.current_char is not None and (self.__is_letter(self.current_char) or self.current_char.isdigit()):
            self.__read_char()
        
        return self.source[position:self.position]
        
    def next_token(self) -> Token:
        tok: Token = None
        
        if self.reading_string:
            tok = self.__new_token(TokenType.STRING, self.__read_string())
            return tok
        
        self.__skip_whitespace()
        
        self.__handle_comments()
        
        if self.current_char not in ['\n', '\r']:
            self.last_was_newline = False
        
        match self.current_char:
            case '\n':
                tok = self.__new_token(TokenType.NEWLINE, "\\n")
                self.last_was_newline = True
                
                if not self.pause:
                    self.line_no += 1
                
            case '\r':
                tok = self.__new_token(TokenType.NEWLINE, "\\r")
                self.last_was_newline = True
                
                if not self.pause:
                    self.line_no += 1
                
            case '(':
                tok = self.__new_token(TokenType.LPAREN, self.current_char)
            case ')':
                tok = self.__new_token(TokenType.RPAREN, self.current_char)
                if self.string_mode:
                    self.reading_string = True
            case '[':
                tok = self.__new_token(TokenType.LBRACKET, self.current_char)
            case ']':
                tok = self.__new_token(TokenType.RBRACKET, self.current_char)
            case '{':
                tok = self.__new_token(TokenType.LBRACE, self.current_char)
            case '}':
                tok = self.__new_token(TokenType.RBRACE, self.current_char)
                
            case ',':
                tok = self.__new_token(TokenType.COMMA, self.current_char)
            case '-':
                tok = self.__new_token(TokenType.NEGATIVE, self.current_char)
                
            case '<':
                tok = self.__new_token(TokenType.STRINGSTART, self.current_char)
                self.string_mode = True
                self.reading_string = True
            case '>':
                tok = self.__new_token(TokenType.STRINGEND, self.current_char)
                self.string_mode = False
                self.reading_string = False
                
            case None:
                tok = self.__new_token(TokenType.EOF, "")
            case _:
                if self.__is_letter(self.current_char):
                    literal: str = clean_grammar_markings(self.__read_identifier())
                    tt: TokenType = lookup_ident(literal)
                    
                    tok = self.__new_token(tt, literal)
                    return tok
                elif self.current_char.isdigit():
                    tok = self.__read_number()
                    return tok
                else:
                    tok = self.__new_token(TokenType.ILLEGAL, self.current_char)
                    
        self.__read_char()
        return tok
    
    def __read_string(self) -> str:
        position: int = self.position
        # In String Mode
        while self.current_char not in ['>', '('] and self.current_char is not None:
            
            # Allow escaping > and (
            if self.current_char == "\\":
                if self.__peek_char() in ['>', "("]:
                    self.__read_char()
            
            self.__read_char()
            
        # print(f"at end of string literal: {self.current_char}")
        self.reading_string = False
        
        string: str = self.source[position:self.position]
        
        new_string = self.__reconstruct_escaped_in_strings(string)
        
        return new_string
    
    def __reconstruct_escaped_in_strings(self, string: str):
        position: int = 0
        result: str = ""
        while position < len(string):
            
            if string[position] == '\\' and position+1 < len(string):
                position += 1
                match string[position]:
                    case '>':
                        result += ">" # clear the slash
                    
                    case 'n':
                        result += '\n'
                    case 't':
                        result += '\t'
                    case 'r':
                        result += '\r'
                    case 'a':
                        result += '\a'
                    case '\\':
                        result += '\\'
                    case _:
                        result += "\\" + string[position]
            else:
                result += string[position]
            position += 1
        
        return result
        
    def __handle_comments(self) -> bool:
        while self.current_char == "/" and self.__peek_char() == "/":
            while self.current_char not in ['\n', '\r'] and self.current_char is not None:
                self.__read_char()
            
            # Handle trailing whitespace
            # print(f"Example print: {self.source[self.position-3:self.position]}")
            self.__skip_whitespace()
            
    
def clean_grammar_markings(candidate):
    if candidate[-2:] in ['ng'] and len(candidate) > 2:
        return candidate[:-2]
    elif candidate[-1] in ['m', 'n', 'b', 'd', 'g'] and len(candidate) > 1:
        return candidate[:-1]
    return candidate