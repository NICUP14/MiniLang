from __future__ import annotations
import enum
from typing import List
from typing import Dict
from typing import Optional
from dataclasses import dataclass
from traceback import print_stack


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

    PRIM = 0
    PTR = 1
    ARR = 2
    STRUCT = 3
    FUN = 4
    STR = 5


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
class VariableType:
    """
    Allows type checking in a structured manner.
    """

    kind: VariableKind
    meta_kind: VariableMetaKind


@dataclass
class Variable:
    """
    Contains the meta-data of a primitive type.
    """

    vtype: VariableType
    off: int
    is_local: bool


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
    ret_type: VariableKind
    off: int
    is_variadic: bool
    is_extern: bool


class NodeKind(enum.Enum):
    """
    Defines all the AST node identifiers.
    """

    IDENT = 1
    INT_LIT = 2
    OP_ADD = 3
    OP_SUB = 4
    OP_MULT = 5
    OP_DIV = 6
    OP_MOD = 7
    OP_ASSIGN = 8
    OP_GT = 9
    OP_LT = 10
    OP_LTE = 11
    OP_GTE = 12
    OP_EQ = 13
    OP_NEQ = 14
    IF = 16
    WHILE = 17
    GLUE = 18
    FUN = 19
    FUN_CALL = 20
    CHAR_LIT = 21
    OP_WIDEN = 22
    RET = 24
    ARR_ACC = 25
    REF = 26
    DEREF = 27
    STR_LIT = 28


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

    def __init__(self, value: str, var_type: VariableType, reg: Register = Register.id_max, loaded: bool = False, imm: bool = False) -> None:
        self.value = value
        self.var_type = var_type
        self.reg = reg
        self.loaded = loaded
        self.imm = imm

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
        return reg_table_at(self.reg, self.var_type.kind)

    def __str__(self) -> str:
        attrs = []
        for key, value in vars(self).items():
            attrs.append(f"{key}={value}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"


#! Warning: Relies on parser state-related variables.
def print_error(loc: str, msg: str):
    from Parser import parser_lines_idx, parser_tokens_idx
    from Parser import curr_line
    line = curr_line().lstrip('\t ').rstrip('\n')
    print()
    print_stack()
    print()
    print(f'location: \"{line}\"')
    print(f'{parser_lines_idx}:{parser_tokens_idx}: {loc}: {msg}')
    exit(1)


def alloc_reg(reg: Register = Register.id_max) -> Register:
    if not reg_is_free(reg):
        print(f'alloc_reg: Unavailable register {reg}')
        exit(1)

    if reg != Register.id_max:
        reg_avail_map[reg] = False
        return reg

    reg = next(filter(lambda reg: reg_avail_map[reg], REGS))
    reg_avail_map[reg] = False

    return reg


def free_reg(reg: Register):
    reg_avail_map[reg] = True


def free_all_regs():
    for reg in REGS:
        free_reg(reg)


def reg_is_free(reg: Register) -> bool:
    return reg_avail_map.get(reg)


def reg_table_at(reg: Register, kind: VariableKind) -> str:
    # if reg == Register.id_max:
    #     print(f'reg_table_at: Invalid register {reg}')
    #     exit(1)

    return REG_TABLE[reg.value][kind.value]


def modf_of(kind: VariableKind) -> str:
    modf_map = {
        VariableKind.INT64: 'q',
        VariableKind.INT32: 'l',
        VariableKind.INT16: 'w',
        VariableKind.INT8: 'b',
    }

    if kind not in modf_map:
        print(f'modf_of: Invalid kind: {kind}')
        exit(1)

    return modf_map[kind]


def global_modf_of(kind: VariableKind) -> str:
    modf_map = {
        VariableKind.INT64: '.quad',
        VariableKind.INT32: '.long',
        VariableKind.INT16: '.short',
        VariableKind.INT8: '.byte',
    }

    if kind not in modf_map:
        print(f'global_modf_of: Invalid kind: {kind}')
        exit(1)

    return modf_map[kind]


def full_name_of(name: str):
    if name in var_map:
        return name
    else:
        return "_".join(label_list + [name])


def off_of(ident: str) -> int:
    if ident not in ident_map:
        print_error('off_of', f'No such indentifier {ident}')
        # print(f'off_of: No such identifier {ident}')
        # exit(1)

    meta_kind = ident_map.get(ident)

    if meta_kind == VariableMetaKind.PRIM:
        return var_map.get(ident).off

    if meta_kind == VariableMetaKind.STR:
        return str_map.get(ident).off

    if meta_kind == VariableMetaKind.ARR:
        return arr_map.get(ident).off

    if meta_kind == VariableMetaKind.PTR:
        return ptr_map.get(ident).off

    print(f'off_of: No such meta kind {meta_kind}')
    exit(1)


# Parses the type of the identifier
def type_of(sym: str) -> VariableType:
    kind_map = {
        'int64': VariableKind.INT64,
        'int32': VariableKind.INT32,
        'int16': VariableKind.INT16,
        'int8': VariableKind.INT8,
        'void': VariableKind.VOID
    }

    if sym not in kind_map:
        print(f'type_of: Invalid type identifier {sym}')
        exit(1)

    return VariableType(kind_map.get(sym), VariableMetaKind.PRIM)


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
        print(f'type_of_ident: No such identifier {ident}')
        exit(1)

    meta_kind = ident_map.get(ident)

    if meta_kind == VariableMetaKind.PRIM:
        return var_map.get(ident).vtype

    if meta_kind == VariableMetaKind.ARR:
        return arr_type

    if meta_kind == VariableMetaKind.PTR:
        return ptr_type

    print(f'type_of_ident: No such meta kind {meta_kind}')
    exit(1)


def type_of_lit(kind: NodeKind):
    type_map = {
        NodeKind.STR_LIT: ptr_type,
        NodeKind.INT_LIT: default_type,
        NodeKind.CHAR_LIT: bool_type,
    }

    if kind not in type_map:
        print(f'type_of_lit: Invalid node kind {kind}')
        exit(1)

    return type_map.get(kind)


def type_of_op(kind: NodeKind) -> VariableType:
    type_map = {
        NodeKind.OP_ADD: default_type,
        NodeKind.OP_SUB: default_type,
        NodeKind.OP_DIV: default_type,
        NodeKind.OP_MOD: default_type,
        NodeKind.OP_GT: bool_type,
        NodeKind.OP_LT: bool_type,
        NodeKind.OP_LTE: bool_type,
        NodeKind.OP_GTE: bool_type,
        NodeKind.OP_EQ: bool_type,
        NodeKind.OP_NEQ: bool_type,
        NodeKind.IF: void_type,
        NodeKind.WHILE: void_type,
        NodeKind.GLUE: void_type,  # ? Temporary
        NodeKind.FUN: void_type,
        NodeKind.FUN_CALL: default_type,
        NodeKind.OP_ASSIGN: default_type,
        NodeKind.ARR_ACC: default_type,
        NodeKind.REF: ptr_type,
        NodeKind.DEREF: default_type
    }

    if kind not in type_map:
        print(f'type_of_op: Invalid node kind {kind}')
        exit(1)

    return type_map.get(kind)


def allowed_op(var_type: VariableType):
    if var_type.meta_kind == VariableMetaKind.PRIM:
        return [
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
            NodeKind.GLUE,
            NodeKind.REF,
        ]

    if var_type == void_type:
        return [
            NodeKind.GLUE,
            NodeKind.REF
        ]

    if var_type == arr_type:
        return [
            NodeKind.DEREF,
            NodeKind.ARR_ACC,
            NodeKind.GLUE,
            NodeKind.REF
        ]

    if var_type == ptr_type:
        return [
            NodeKind.GLUE,
            NodeKind.ARR_ACC,
            NodeKind.DEREF,
            NodeKind.REF
        ]

    print(f'allowed_op: Invalid type: {var_type}')
    exit(1)


def needs_widen(var_type: VariableType, var_type2: VariableType):
    if var_type == var_type2:
        return 0

    if var_type == ptr_type or var_type2 == ptr_type:
        return 0

    if var_type == arr_type or var_type2 == arr_type:
        return 0

    if var_type == void_type or var_type2 == void_type:
        return 0

    if var_type.meta_kind == VariableMetaKind.PRIM and var_type2.meta_kind == VariableMetaKind.PRIM:
        return (2 if cmp_var_kind(var_type.kind, var_type2.kind) else 1)

    print(f'needs_widen: Invalid type in ({var_type, var_type2})')
    exit(1)


def size_of(var_type: VariableType):
    if var_type == ptr_type:
        return 8

    if var_type == arr_type:
        return 8

    if var_type.meta_kind == VariableMetaKind.PRIM:
        size_map = {
            VariableKind.INT64: 8,
            VariableKind.INT32: 4,
            VariableKind.INT16: 2,
            VariableKind.INT8: 1,
            VariableKind.VOID: 0,
        }

        if var_type.kind in size_map:
            return size_map.get(var_type.kind)

    print(f'size_of: Invalid variable type {var_type}')
    exit(1)


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
        print(f'cmp_modf_of: Invalid kind: {kind}')
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

var_off = 0
var_map: Dict[str, Variable] = dict()
fun_map: Dict[str, Function] = dict()
arr_map: Dict[str, Array] = dict()
ptr_map: Dict[str, Pointer] = dict()
str_map: Dict[str, String] = dict()
ident_map: Dict[str, VariableMetaKind] = dict()
str_lit_map: Dict[str, str] = dict()
reg_avail_map = {reg: True for reg in REGS}
label_list: List[str] = []
ptr_type = VariableType(VariableKind.INT64, VariableMetaKind.PTR)
arr_type = VariableType(VariableKind.INT64, VariableMetaKind.ARR)
void_type = VariableType(VariableKind.VOID, VariableMetaKind.PRIM)
bool_type = VariableType(VariableKind.INT8, VariableMetaKind.PRIM)
default_type = VariableType(VariableKind.INT64, VariableMetaKind.PRIM)
fun_name = ''
