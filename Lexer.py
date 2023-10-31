import re
import enum
from typing import List
from dataclasses import dataclass

OPERATORS = (
    '+',
    '-',
    '*',
    '/',
    '%',
    '==',
    '!=',
    '=',
    '>=',
    '<=',
    '>',
    '<',
    '(',
    ')',
    ':',
    ',',
    '[',
    ']',
    '&'
)


def to_pattern(l): return '|'.join(l)
def is_int(s: str): return re.search(INT_PATTERN, s) is not None


INT_PATTERN = r'-?\d+'
CHAR_PATTERN = r'\'.+\''
STR_PATTERN = r'\".+\"'
SYM_PATTERN = r'\w+'
OP_PATTERN = to_pattern(map(re.escape, OPERATORS))
PATTERN = to_pattern([
    INT_PATTERN,
    CHAR_PATTERN,
    STR_PATTERN,
    SYM_PATTERN,
    OP_PATTERN
])


class TokenKind(enum.Enum):
    INT_LIT = 0
    PLUS = 1
    MINUS = 2
    MULT = 3
    DIV = 4
    PERC = 5
    EQ = 6
    GT = 7
    GTE = 8
    LT = 9
    LTE = 10
    NEQ = 11
    ASSIGN = 12
    IDENT = 13
    LPAREN = 14
    RPAREN = 15
    KW_LET = 16
    KW_IF = 17
    KW_ELSE = 18
    KW_WHILE = 19
    KW_END = 20
    KW_FUN = 21
    KW_VOID = 22
    KW_INT64 = 23
    COLON = 24
    COMMA = 25
    FUN_CALL = 26
    CHAR_LIT = 27
    KW_CHAR = 28
    KW_INT32 = 29,
    KW_INT16 = 30,
    KW_INT8 = 31
    KW_RET = 32
    LBRACE = 33
    RBRACE = 34
    KW_AT = 35
    AMP = 36
    DEREF = 37
    STR_LIT = 38
    KW_EXTERN = 39


@dataclass
class Token:
    kind: TokenKind
    value: str


TOKEN_KIND_MAP = {
    '+': TokenKind.PLUS,
    '-': TokenKind.MINUS,
    '*': TokenKind.MULT,
    '/': TokenKind.DIV,
    '%': TokenKind.PERC,
    '=': TokenKind.ASSIGN,
    '==': TokenKind.EQ,
    '!=': TokenKind.NEQ,
    '<=': TokenKind.LTE,
    '>=': TokenKind.GTE,
    '<': TokenKind.LT,
    '>': TokenKind.GT,
    '(': TokenKind.LPAREN,
    ')': TokenKind.RPAREN,
    ':': TokenKind.COLON,
    ',': TokenKind.COMMA,
    '[': TokenKind.LBRACE,
    ']': TokenKind.RBRACE,
    '&': TokenKind.AMP,
    'at': TokenKind.KW_AT,
    'let': TokenKind.KW_LET,
    'if': TokenKind.KW_IF,
    'else': TokenKind.KW_ELSE,
    'while': TokenKind.KW_WHILE,
    'end': TokenKind.KW_END,
    'fun': TokenKind.KW_FUN,
    'void': TokenKind.KW_VOID,
    'int64': TokenKind.KW_INT64,
    'int32': TokenKind.KW_INT32,
    'int16': TokenKind.KW_INT16,
    'int8': TokenKind.KW_INT8,
    'char': TokenKind.KW_CHAR,
    'ret': TokenKind.KW_RET,
    'extern': TokenKind.KW_EXTERN
}


def token_is_param(kind: TokenKind) -> bool:
    return kind in (
        TokenKind.INT_LIT,
        TokenKind.CHAR_LIT,
        TokenKind.STR_LIT,
        TokenKind.IDENT
    )


def token_is_op(kind: TokenKind) -> bool:
    return kind in (
        TokenKind.PLUS,
        TokenKind.MINUS,
        TokenKind.MULT,
        TokenKind.DIV,
        TokenKind.PERC,
        TokenKind.ASSIGN,
        TokenKind.EQ,
        TokenKind.NEQ,
        TokenKind.GT,
        TokenKind.LT,
        TokenKind.GTE,
        TokenKind.LTE,
        TokenKind.COMMA,
        TokenKind.KW_AT,
        TokenKind.AMP,
        TokenKind.DEREF,
        TokenKind.FUN_CALL
    )


def token_is_paren(kind: TokenKind) -> bool:
    return kind in (
        TokenKind.LPAREN,
        TokenKind.RPAREN
    )


def token_kind_of(value: str) -> TokenKind:
    if value in TOKEN_KIND_MAP:
        return TOKEN_KIND_MAP.get(value)
    if value.startswith('\'') and value.endswith('\''):
        return TokenKind.CHAR_LIT
    if value.startswith('\"') and value.endswith('\"'):
        return TokenKind.STR_LIT
    if str.isdigit(value):
        return TokenKind.INT_LIT
    if str.isalnum(value):
        return TokenKind.IDENT

    print(f'token_kind_of: Invalid token {value}')
    exit(1)


def token_is_rassoc(kind: TokenKind) -> bool:
    if not token_is_op(kind):
        print(f'token_is_rassoc: Invalid operator kind {kind}')

    return kind == TokenKind.ASSIGN


def token_is_bin_op(kind: TokenKind) -> bool:
    if not token_is_op(kind):
        print(f'token_is_bin_op: Invalid operator kind {kind}')

    return kind in [
        TokenKind.PLUS,
        TokenKind.MINUS,
        TokenKind.MULT,
        TokenKind.DIV,
        TokenKind.PERC,
        TokenKind.EQ,
        TokenKind.GT,
        TokenKind.GTE,
        TokenKind.LT,
        TokenKind.LTE,
        TokenKind.NEQ,
        TokenKind.ASSIGN,
        TokenKind.COMMA,
        TokenKind.KW_AT,
    ]


def token_is_unary_op(kind: TokenKind) -> bool:
    if not token_is_op(kind):
        print(f'token_is_bin_op: Invalid operator kind {kind}')

    return kind in [
        TokenKind.DEREF,
        TokenKind.AMP,
        TokenKind.FUN_CALL
    ]


def to_token(value: str) -> Token:
    return Token(token_kind_of(value), value)


def tokenize(line: str):
    return list(map(to_token, re.findall(PATTERN, line)))


def post_process(tokens: List[Token]):
    def process(token: Token):
        if token.kind == TokenKind.RBRACE:
            return (Token(TokenKind.RPAREN, ')'),)
        if token.kind == TokenKind.LBRACE:
            return (Token(TokenKind.KW_AT, 'at'), Token(TokenKind.LPAREN, '('))
        return (token,)

    def flat_map(f, xs): return [y for ys in xs for y in f(ys)]

    if tokens.count(Token(TokenKind.LBRACE, '[')) != tokens.count(Token(TokenKind.RBRACE, ']')):
        print('post_process: Expression contains unclosed braces')

    return flat_map(process, tokens)
