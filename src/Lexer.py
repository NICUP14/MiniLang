import re
import enum
from typing import List
from typing import Optional
from dataclasses import dataclass
from Def import print_error


OPERATORS = (
    '<<-',
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
    '&',
    '...',
)


def to_pattern(l):
    return '|'.join(l)


def is_int(s: str):
    return re.search(INT_PATTERN, s) is not None


INT_PATTERN = r'-?\d+'
CHAR_PATTERN = r'\'[^\']+\''
STR_PATTERN = r'\"[^\"]*\"'
SYM_PATTERN = r'\\?\w+'
OP_PATTERN = to_pattern(map(re.escape, OPERATORS))
PATTERN = to_pattern([
    INT_PATTERN,
    CHAR_PATTERN,
    STR_PATTERN,
    SYM_PATTERN,
    OP_PATTERN
])


class TokenKind(enum.Enum):
    INT_LIT = enum.auto()
    CHAR_LIT = enum.auto()
    STR_LIT = enum.auto()
    PLUS = enum.auto()
    MINUS = enum.auto()
    MULT = enum.auto()
    DIV = enum.auto()
    PERC = enum.auto()
    EQ = enum.auto()
    GT = enum.auto()
    GTE = enum.auto()
    LT = enum.auto()
    LTE = enum.auto()
    NEQ = enum.auto()
    ASSIGN = enum.auto()
    IDENT = enum.auto()
    LPAREN = enum.auto()
    RPAREN = enum.auto()
    LBRACE = enum.auto()
    RBRACE = enum.auto()
    AMP = enum.auto()
    OR = enum.auto()
    AND = enum.auto()
    DEREF = enum.auto()
    COLON = enum.auto()
    COMMA = enum.auto()
    PER_FUN = enum.auto()
    FUN_CALL = enum.auto()
    HEREDOC = enum.auto()
    KW_AT = enum.auto()
    KW_LET = enum.auto()
    KW_IF = enum.auto()
    KW_ELSE = enum.auto()
    KW_WHILE = enum.auto()
    KW_END = enum.auto()
    KW_FUN = enum.auto()
    KW_RET = enum.auto()
    KW_VOID = enum.auto()
    KW_INT16 = enum.auto()
    KW_INT32 = enum.auto()
    KW_INT64 = enum.auto()
    KW_INT8 = enum.auto()
    KW_EXTERN = enum.auto()
    KW_TYPEDEF = enum.auto()
    KW_IMPORT = enum.auto()
    KW_DEFER = enum.auto()
    KW_ASM = enum.auto()


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
    '&': TokenKind.AND,
    '|': TokenKind.OR,
    '...': TokenKind.PER_FUN,
    '<<-': TokenKind.HEREDOC,
    '\\end': TokenKind.IDENT,
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
    'ret': TokenKind.KW_RET,
    'extern': TokenKind.KW_EXTERN,
    'typedef': TokenKind.KW_TYPEDEF,
    # 'defer': TokenKind.KW_DEFER
    'import': TokenKind.KW_IMPORT,
    'asm': TokenKind.KW_ASM
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
        TokenKind.AND,
        TokenKind.OR,
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
        TokenKind.FUN_CALL,
        TokenKind.KW_ASM
    )


def token_is_paren(kind: TokenKind) -> bool:
    return kind in (
        TokenKind.LPAREN,
        TokenKind.RPAREN
    )


def token_kind_of(value: str) -> Optional[TokenKind]:
    if value in TOKEN_KIND_MAP:
        return TOKEN_KIND_MAP.get(value)
    if value.startswith('\'') and value.endswith('\''):
        return TokenKind.CHAR_LIT
    if value.startswith('\"') and value.endswith('\"'):
        return TokenKind.STR_LIT
    if str.isdigit(value):
        return TokenKind.INT_LIT
    if str.isalnum(value.replace('_', '')):
        return TokenKind.IDENT

    print_error('token_kind_of', f'Invalid token {value}')
    return None


def token_is_rassoc(kind: TokenKind) -> bool:
    return kind == TokenKind.ASSIGN


def token_is_bin_op(kind: TokenKind) -> bool:
    if not token_is_op(kind):
        print_error('token_is_bin_op', f'Invalid operator kind {kind}')

    return kind in [
        TokenKind.PLUS,
        TokenKind.MINUS,
        TokenKind.MULT,
        TokenKind.DIV,
        TokenKind.PERC,
        TokenKind.AND,
        TokenKind.OR,
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
        print_error('token_is_bin_op', f'Invalid operator kind {kind}')

    return kind in [
        TokenKind.DEREF,
        TokenKind.AMP,
        TokenKind.KW_ASM,
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

    def flat_map(f, xs):
        return [y for ys in xs for y in f(ys)]

    if tokens.count(Token(TokenKind.LBRACE, '[')) != tokens.count(Token(TokenKind.RBRACE, ']')):
        print_error('post_process', 'Expression contains unclosed braces')

    return flat_map(process, tokens)
