from __future__ import annotations
import sys
import enum
from typing import List
from typing import Dict
from typing import Optional
from dataclasses import dataclass
from traceback import print_stack


class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Register(enum.Enum):
    """
    Defines all possible assembly registers.
    `Register.id_max` holds the total register count.
    """

    rax = 0
    rbx = 1
    rcx = 2
    rdx = 3
    rsi = 4
    rdi = 5
    r8 = 6
    r9 = 7
    r10 = 8
    r11 = 9
    r12 = 10
    r13 = 11
    r14 = 12
    r15 = 13
    id_max = 14


class VariableMetaKind(enum.Enum):
    """
    Defines all possible structural types.
    Meta-kinds are used internally to distinguish
    between primitives, advanced or composite types.
    """

    PRIM = enum.auto()
    PTR = enum.auto()
    ARR = enum.auto()
    FUN = enum.auto()
    STRUCT = enum.auto()


class VariableKind(enum.Enum):
    """
    Defines all possible primitive types.
    """

    INT64 = 0
    INT32 = 1
    INT16 = 2
    INT8 = 3
    VOID = 4


@dataclass
class VariableCompKind:
    kind: VariableKind
    meta_kind: VariableMetaKind


class VariableType:
    """
    Allows type checking in a structured manner.
    """

    def __init__(self, ckind: VariableCompKind, elem_ckind: VariableCompKind = VariableCompKind(VariableKind.INT64, VariableMetaKind.PRIM)) -> None:
        self.ckind = ckind
        self.elem_ckind = elem_ckind

    def __eq__(self, other):
        if isinstance(other, VariableType):
            return (self.ckind, self.elem_ckind) == (other.ckind, self.elem_ckind)
        return False

    def __str__(self) -> str:
        attrs = []
        for key, value in vars(self).items():
            attrs.append(f"{key}={value}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def kind(self):
        return self.ckind.kind

    def meta_kind(self):
        return self.ckind.meta_kind


class Variable:
    """
    Contains the meta-data of a primitive type.
    """

    # ? The value field is used to initialize global variables
    def __init__(self, vtype: VariableType, off: int, is_local: bool = True, value: int = 0):
        self.vtype = vtype
        self.off = off
        self.is_local = is_local
        self.value = value


@dataclass
class Pointer:
    """
    Contains the meta-data of a pointer type.
    """

    name: str
    elem_type: VariableType
    off: int


@dataclass
class Array:
    """
    Contains the meta-data of an array type.
    """

    name: str
    elem_cnt: int
    elem_type: VariableType
    off: int


@dataclass
class String:
    """
    Contains the meta-data of an array type.
    """

    name: str
    off: int


@dataclass
class Function:
    """
    Contains the meta-data of a function type.
    """

    name: str
    arg_cnt: int
    arg_names: List[str]
    arg_types: List[VariableType]
    ret_type: VariableCompKind
    off: int
    is_variadic: bool
    is_extern: bool


class NodeKind(enum.Enum):
    """
    Defines all the AST node identifiers.
    """

    IDENT = enum.auto()
    INT_LIT = enum.auto()
    OP_ADD = enum.auto()
    OP_SUB = enum.auto()
    OP_MULT = enum.auto()
    OP_DIV = enum.auto()
    OP_MOD = enum.auto()
    OP_AND = enum.auto()
    OP_OR = enum.auto()
    OP_ASSIGN = enum.auto()
    OP_GT = enum.auto()
    OP_LT = enum.auto()
    OP_LTE = enum.auto()
    OP_GTE = enum.auto()
    OP_EQ = enum.auto()
    OP_NEQ = enum.auto()
    IF = enum.auto()
    WHILE = enum.auto()
    GLUE = enum.auto()
    FUN = enum.auto()
    FUN_CALL = enum.auto()
    CHAR_LIT = enum.auto()
    OP_WIDEN = enum.auto()
    RET = enum.auto()
    ARR_ACC = enum.auto()
    REF = enum.auto()
    DEREF = enum.auto()
    STR_LIT = enum.auto()
    DEFER = enum.auto()
    ASM = enum.auto()


class Node:
    """
    Represents a node of the AST (operation).
    """

    def __init__(self, kind: NodeKind, ntype: VariableType, value: str, left: Node = None, right: Node = None, middle: Node = None):
        self.kind = kind
        self.ntype = ntype
        self.value = value
        self.left = left
        self.right = right
        self.middle = middle

    def __str__(self) -> str:
        attrs = []
        for key, value in vars(self).items():
            attrs.append(f"{key}={value}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"


class Operand:
    """
    Represents an operand of the AST node (operation).
    Operands are used internally in the code generator (Gen.py)
    to standardize snippet creation (`gen_*` functions return a list of snippets).
    """

    def __init__(self, value: str, var_type: VariableType, reg: Register = Register.id_max, loaded: bool = False, imm: bool = False, ref: bool = False) -> None:
        self.value = value
        self.var_type = var_type
        self.reg = reg
        self.loaded = loaded
        self.imm = imm
        self.ref = ref

    def is_ref(self) -> bool:
        return self.ref

    def is_imm(self) -> bool:
        return self.imm

    def is_loaded(self) -> bool:
        return self.loaded

    def load(self):
        self.loaded = True
        return self

    def unload(self):
        self.loaded = False
        return self

    def reg_str(self):
        return reg_table_at(self.reg, self.var_type.kind())

    def __str__(self) -> str:
        attrs = []
        for key, value in vars(self).items():
            attrs.append(f"{key}={value}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"


def color_str(color: Color, msg: str):
    if not color_enabled:
        return msg
    return f'{color}{msg}{Color.ENDC}'


#! Warning: Relies on parser state-related variables.
def print_error(loc: str, msg: str, parser=None):
    line = ('' if parser is None or parser.no_more_lines() else '\"' +
            parser.curr_line().lstrip('\t ').rstrip('\n') + '\"')
    desc = color_str(Color.FAIL, f'{loc}: {msg}')
    print()
    print_stack()
    print()
    if parser is not None:
        print(f'location: {color_str(Color.FAIL, line)}')
        print(f'{parser.source}:{parser.lines_idx}:{parser.tokens_idx}: {desc}')
    else:
        print(f'ERROR: {desc}')
    exit(1)


def print_stdout(msg: str = ''):
    print(msg, file=stdout)


def alloc_reg(reg: Register = Register.id_max, opd: Operand = None) -> Register:
    if not reg_is_free(reg):
        print_error('alloc_reg', f'Unavailable register {reg}')

    if reg != Register.id_max:
        reg_avail_map[reg] = False
        if opd is not None:
            opd_map[reg] = opd

        return reg

    reg = next(filter(lambda reg: reg_avail_map[reg], REGS))
    reg_avail_map[reg] = False
    if opd is not None:
        opd_map[reg] = opd

    return reg


def free_reg(reg: Register):
    opd_map[reg] = None
    reg_avail_map[reg] = True


def free_all_regs():
    for reg in REGS:
        free_reg(reg)


def reg_is_free(reg: Register) -> bool:
    return reg_avail_map.get(reg)


def reg_table_at(reg: Register, kind: VariableKind) -> str:
    if reg == Register.id_max:
        print_error('reg_table_at', f'Invalid register {reg}')

    return REG_TABLE[reg.value][kind.value]


def modf_of(kind: VariableKind) -> str:
    modf_map = {
        VariableKind.INT64: 'q',
        VariableKind.INT32: 'l',
        VariableKind.INT16: 'w',
        VariableKind.INT8: 'b',
    }

    if kind not in modf_map:
        print_error('modf_of', f'Invalid kind: {kind}')

    return modf_map[kind]


def global_modf_of(kind: VariableKind) -> str:
    modf_map = {
        VariableKind.INT64: '.quad',
        VariableKind.INT32: '.long',
        VariableKind.INT16: '.short',
        VariableKind.INT8: '.byte',
    }

    if kind not in modf_map:
        print_error('global_modf_of', f'Invalid kind: {kind}')

    return modf_map[kind]


def full_name_of(name: str):
    if name in var_map:
        return name
    else:
        return "_".join(label_list + [name])


def off_of(ident: str) -> int:
    if ident not in ident_map:
        print_error('off_of', f'No such identifier {ident}')

    meta_kind = ident_map.get(ident)

    if meta_kind == VariableMetaKind.PRIM:
        return var_map.get(ident).off

    if meta_kind == VariableMetaKind.ARR:
        return arr_map.get(ident).off

    if meta_kind == VariableMetaKind.PTR:
        return ptr_map.get(ident).off

    print_error('off_of', f'No such meta kind {meta_kind}')


# Parses the type of the identifier
def type_of(sym: str, use_mkind: bool = True) -> VariableType:
    if sym not in ckind_map:
        print_error('type_of', f'Invalid type identifier {sym}')

    ckind = ckind_map.get(sym)
    meta_kind = VariableMetaKind.PRIM if not use_mkind else ckind.meta_kind
    return VariableType(VariableCompKind(ckind.kind, meta_kind))


def rev_type_of_ident(name: str) -> str:
    rev_kind_map = {
        VariableKind.INT64: 'int64',
        VariableKind.INT32: 'int32',
        VariableKind.INT16: 'int16',
        VariableKind.INT8: 'int8',
        VariableKind.VOID: 'void',
    }

    if name not in ident_map:
        print_error('rev_type_of_ident', f'No such identifier {name}')

    meta_kind = ident_map.get(name)
    if meta_kind == VariableMetaKind.PRIM:
        if name not in var_map:
            print_error('rev_type_of_ident', f'No such variable {name}')

        var = var_map.get(name)
        return rev_kind_map.get(var.vtype.kind())

    if meta_kind == VariableMetaKind.PTR:
        if name not in ptr_map:
            print_error('rev_type_of_ident', f'No such pointer {name}')

        ptr = ptr_map.get(name)
        return f'{rev_kind_map.get(ptr.elem_type.kind())}*'

    if meta_kind == VariableMetaKind.ARR:
        if name not in arr_map:
            print_error('rev_type_of_ident', f'No such array {name}')

        arr = arr_map.get(name)
        return f'{rev_kind_map.get(arr.elem_type.kind())}[{arr.elem_cnt}]'

    print_error('rev_type_of_ident', f'No such meta kind {meta_kind}')


def rev_type_of(vtype: VariableType) -> str:
    rev_kind_map = {
        VariableKind.INT64: 'int64',
        VariableKind.INT32: 'int32',
        VariableKind.INT16: 'int16',
        VariableKind.INT8: 'int8',
        VariableKind.VOID: 'void',
    }

    if vtype.kind() not in rev_kind_map:
        print_error('rev_type_of', f'Invalid variable kind {vtype.kind}')

    if vtype.ckind == ptr_ckind:
        return f'*{rev_kind_map.get(vtype.elem_ckind.kind)}'

    if vtype.ckind == arr_ckind:
        return f'{rev_kind_map.get(vtype.elem_ckind.kind)}[]'

    return rev_kind_map.get(vtype.kind())


def cmp_var_kind(kind: VariableKind, kind2: VariableKind):
    precedence_map = {
        VariableKind.INT64: 4,
        VariableKind.INT32: 3,
        VariableKind.INT16: 2,
        VariableKind.INT8: 1,
        VariableKind.VOID: 0,
    }

    return precedence_map.get(kind) > precedence_map.get(kind2)


def type_of_ident(ident: str) -> VariableType:
    if ident not in ident_map:
        print_error('type_of_ident', f'No such identifier {ident}')

    meta_kind = ident_map.get(ident)

    if meta_kind == VariableMetaKind.ARR:
        if ident not in arr_map:
            print_error('type_of_ident', f'No such variable {ident}')

        return VariableType(arr_ckind, arr_map.get(ident).elem_type.ckind)

    if meta_kind == VariableMetaKind.PTR:
        if ident not in ptr_map:
            print_error('type_of_ident', f'No such variable {ident}')

        return VariableType(ptr_ckind, ptr_map.get(ident).elem_type.ckind)

    if meta_kind == VariableMetaKind.PRIM:
        if ident not in var_map:
            print_error('type_of_ident', f'No such variable {ident}')

        return var_map.get(ident).vtype

    print_error('type_of_ident', f'No such meta kind {meta_kind}')


def type_of_lit(kind: NodeKind) -> VariableType:
    type_map = {
        NodeKind.STR_LIT: ptr_ckind,
        NodeKind.INT_LIT: default_ckind,
        NodeKind.CHAR_LIT: bool_ckind,
    }

    if kind not in type_map:
        print_error('type_of_lit', f'Invalid node kind {kind}')

    return VariableType(type_map.get(kind), default_ckind)


def type_of_op(kind: NodeKind) -> VariableType:
    ckind_map = {
        NodeKind.OP_MULT: default_ckind,
        NodeKind.OP_ADD: default_ckind,
        NodeKind.OP_SUB: default_ckind,
        NodeKind.OP_DIV: default_ckind,
        NodeKind.OP_MOD: default_ckind,
        NodeKind.OP_AND: default_ckind,
        NodeKind.OP_OR: default_ckind,
        NodeKind.OP_GT: bool_ckind,
        NodeKind.OP_LT: bool_ckind,
        NodeKind.OP_LTE: bool_ckind,
        NodeKind.OP_GTE: bool_ckind,
        NodeKind.OP_EQ: bool_ckind,
        NodeKind.OP_NEQ: bool_ckind,
        NodeKind.IF: void_ckind,
        NodeKind.WHILE: void_ckind,
        NodeKind.GLUE: void_ckind,
        NodeKind.FUN: void_ckind,
        NodeKind.ASM: void_ckind,
        NodeKind.FUN_CALL: default_ckind,
        NodeKind.OP_ASSIGN: default_ckind,
        NodeKind.ARR_ACC: default_ckind,
        NodeKind.REF: ptr_ckind,
        NodeKind.DEREF: default_ckind
    }

    if kind not in ckind_map:
        print_error('type_of_op', f'Invalid node kind {kind}')

    return VariableType(ckind_map.get(kind), default_ckind)


def allowed_op(ckind: VariableCompKind):
    if ckind.meta_kind == VariableMetaKind.PRIM:
        return [
            NodeKind.OP_ADD,
            NodeKind.OP_SUB,
            NodeKind.OP_MULT,
            NodeKind.OP_DIV,
            NodeKind.OP_MOD,
            NodeKind.OP_AND,
            NodeKind.OP_OR,
            NodeKind.OP_ASSIGN,
            NodeKind.OP_GT,
            NodeKind.OP_LT,
            NodeKind.OP_LTE,
            NodeKind.OP_GTE,
            NodeKind.OP_EQ,
            NodeKind.OP_NEQ,
            NodeKind.GLUE,
            NodeKind.REF,
        ]

    if ckind == void_ckind:
        return [
            NodeKind.GLUE,
            NodeKind.REF
        ]

    if ckind == arr_ckind:
        return [
            NodeKind.OP_ADD,
            NodeKind.OP_SUB,
            NodeKind.DEREF,
            NodeKind.ARR_ACC,
            NodeKind.GLUE,
            NodeKind.REF
        ]

    if ckind == ptr_ckind:
        return [
            NodeKind.GLUE,
            NodeKind.ARR_ACC,
            NodeKind.OP_ADD,
            NodeKind.OP_SUB,
            NodeKind.OP_MULT,
            NodeKind.OP_DIV,
            NodeKind.OP_MOD,
            NodeKind.OP_ASSIGN,
            NodeKind.OP_GT,
            NodeKind.OP_LT,
            NodeKind.OP_LTE,
            NodeKind.OP_GTE,
            NodeKind.OP_EQ,
            NodeKind.OP_NEQ,
            NodeKind.DEREF,
            NodeKind.REF
        ]

    print_error('allowed_op', f'Invalid type: {ckind}')


def needs_widen(ckind: VariableCompKind, ckind2: VariableCompKind):
    if ckind == ckind2:
        return 0

    if ckind == ptr_ckind or ckind2 == ptr_ckind:
        return 0

    if ckind == arr_ckind or ckind2 == arr_ckind:
        return 0

    if ckind == void_ckind or ckind2 == void_ckind:
        return 0

    if ckind.meta_kind == VariableMetaKind.PRIM and ckind2.meta_kind == VariableMetaKind.PRIM:
        return (2 if cmp_var_kind(ckind.kind, ckind2.kind) else 1)

    print_error('needs_widen', f'Invalid composite kinds ({ckind, ckind2})')


def size_of(ckind: VariableCompKind):
    if ckind in (ptr_ckind, arr_ckind):
        return 8

    if ckind.meta_kind == VariableMetaKind.PRIM:
        size_map = {
            VariableKind.INT64: 8,
            VariableKind.INT32: 4,
            VariableKind.INT16: 2,
            VariableKind.INT8: 1,
            VariableKind.VOID: 0,
        }

        if ckind.kind in size_map:
            return size_map.get(ckind.kind)

    print_error('size_of', f'Invalid variable type {ckind}')


def cmp_modf_of(kind: NodeKind) -> str:
    modf_map = {
        NodeKind.OP_EQ: 'e',
        NodeKind.OP_NEQ: 'ne',
        NodeKind.OP_GT: 'g',
        NodeKind.OP_LT: 'l',
        NodeKind.OP_GTE: 'ge',
        NodeKind.OP_LTE: 'le'
    }

    if kind not in modf_map:
        print_error('cmp_modf_of', f'Invalid kind: {kind}')
    return modf_map[kind]


REG_TABLE = (
    ('%rax', '%eax', '%ax', '%al'),
    ('%rbx', '%ebx', '%bx', '%bl'),
    ('%rcx', '%ecx', '%cx', '%cl'),
    ('%rdx', '%edx', '%dx', '%dl'),
    ('%rsi', '%esi', '%si', '%sil'),
    ('%rdi', '%edi', '%di', '%dil'),
    ('%r8', '%r8d', '%r8w', '%r8b'),
    ('%r9', '%r9d', '%r9w', '%r9b'),
    ('%r10', '%r10d', '%r10w', '%r10b'),
    ('%r11', '%r11d', '%r11w', '%r11b'),
    ('%r12', '%r12d', '%r12w', '%r12b'),
    ('%r13', '%r13d', '%r13w', '%r13b'),
    ('%r14', '%r14d', '%r14w', '%r14b'),
    ('%r15', '%r15d', '%r15w', '%r15b'),
)

REGS = (
    Register.rax,
    Register.rbx,
    Register.rcx,
    Register.rdx,
    Register.rsi,
    Register.rdi,
    Register.r8,
    Register.r9,
    Register.r10,
    Register.r11,
    Register.r12,
    Register.r13,
    Register.r14,
    Register.r15,
    Register.id_max,
)

CALL_REGS = (
    Register.rdi,
    Register.rsi,
    Register.rdx,
    Register.rcx,
    Register.r8,
    Register.r9
)

# Configuration flag
color_enabled = True
comments_enabled = True
stdout = sys.stdout

ckind_map = {
    'int64': VariableCompKind(VariableKind.INT64, VariableMetaKind.PRIM),
    'int32': VariableCompKind(VariableKind.INT32, VariableMetaKind.PRIM),
    'int16': VariableCompKind(VariableKind.INT16, VariableMetaKind.PRIM),
    'int8': VariableCompKind(VariableKind.INT8, VariableMetaKind.PRIM),
    'void': VariableCompKind(VariableKind.VOID, VariableMetaKind.PRIM)
}

var_off = 0
var_map: Dict[str, Variable] = dict()
fun_map: Dict[str, Function] = dict()
arr_map: Dict[str, Array] = dict()
ptr_map: Dict[str, Pointer] = dict()
str_map: Dict[str, String] = dict()
ident_map: Dict[str, VariableMetaKind] = dict()
str_lit_map: Dict[str, str] = dict()
opd_map = {reg: None for reg in REGS}
reg_avail_map = {reg: True for reg in REGS}
label_list: List[str] = []
ptr_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.PTR)
arr_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.ARR)
void_ckind = VariableCompKind(VariableKind.VOID, VariableMetaKind.PRIM)
bool_ckind = VariableCompKind(VariableKind.INT8, VariableMetaKind.PRIM)
default_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.PRIM)
fun_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.FUN)
void_type = VariableType(void_ckind)
bool_type = VariableType(bool_ckind)
default_type = VariableType(default_ckind)
fun_name = ''
