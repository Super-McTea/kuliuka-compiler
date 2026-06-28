from enum import Enum
from typing import Any

class TokenType(Enum):
    
    # Special Tokens
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"
    
    # Special Symbols
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    
    COMMA = "COMMA"
    
    # Data Types
    IDENT = "IDENT"
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    VOID = "VOID"
    
    # Keywords
    # LET = "LET"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    IMPORT = "IMPORT"
    
    STRINGSTART = "STRINGSTART"
    STRINGEND = "STRINGEND"
    
    IS = "IS"
    # SAY = "SAY"
    WHEN = "WHEN"
    AGAIN = "AGAIN"
    IF = "IF"
    ELSE = "ELSE"
    END = "END"
    
    NEWLINE = "NEWLINE"
    
    NEGATIVE = "NEGATIVE"
    
    TRUE = "TRUE"
    FALSE = "FALSE"
    
    # Typing
    TYPE = "TYPE"
    
    # Arithmetics
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    
    # Comparisons
    MORE = "MORE"
    LESS = "LESS"
    EQLS = "EQLS"
    NOT = "NOT"
    
class Token:
    def __init__(self, type: TokenType, literal: Any, line_no: int, position: int) -> None:
        self.type = type
        self.literal = literal
        self.line_no = line_no
        self.position = position
    
    def __str__(self) -> str:
        return f"Token[{self.type} : {self.literal} : Line {self.line_no} : Position {self.position}]"
    
    def __repr__(self):
        return str(self)
    
KEYWORDS: dict[str, TokenType] = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    ",": TokenType.COMMA,
    "<": TokenType.STRINGSTART,
    ">": TokenType.STRINGEND,
    "-": TokenType.NEGATIVE,
    
    # "let": TokenType.LET,
    "bulami": TokenType.FUNCTION,
    "zagu": TokenType.RETURN,
    "zhibalia": TokenType.IMPORT,
    
    "ki": TokenType.IS,
    # "lia": TokenType.SAY,
    "nuliama": TokenType.IF,
    "kiia": TokenType.WHEN,
    "kika": TokenType.AGAIN,
    "favu": TokenType.ELSE,
    "katiu": TokenType.END,
    
    "wogi": TokenType.TRUE,
    "muda": TokenType.FALSE,
    
    "tuthi": TokenType.ADD,
    "kima": TokenType.SUB,
    "batidi": TokenType.MUL,
    "nauki": TokenType.DIV,
    
    "bufani": TokenType.MORE,
    "ikuzu": TokenType.LESS,
    "nugiazu": TokenType.EQLS,
    "maba": TokenType.NOT
}

TYPE_KEYWORDS: dict[str, TokenType] = {
    "akatanami": TokenType.INT,
    "vadriuka": TokenType.FLOAT,
    "lana": TokenType.STRING,
    "zuruva": TokenType.BOOLEAN,
    "tidimaba": TokenType.VOID
}

def lookup_ident(ident: str) -> TokenType:
    tt: TokenType | None = KEYWORDS.get(ident)
    if tt is not None:
        return tt
    
    if ident in TYPE_KEYWORDS:
        return TokenType.TYPE
    
    return TokenType.IDENT