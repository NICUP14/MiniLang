from __future__ import annotations
import sys
import enum
from typing import Any
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
    WARNING = '\033[35m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Register(enum.Enum):
    """
    Defines all possible assembly registers.
    `Register.id_max` holds the total register count.
    """

    rbx = 0
    rcx = 1
    rsi = 2
    rdi = 3
    r8 = 4
    r9 = 5
    r10 = 6
    r11 = 7
    r12 = 8
    r13 = 9
    r14 = 10
    r15 = 11
    rax = 12
    rdx = 13
    id_max = 14


class VariableMetaKind(enum.Enum):
    """
    Defines all possible structural types.
    Meta-kinds are used internally to distinguish
    between primitives, advanced or composite types.
    """

    ANY = enum.auto()
    BOOL = enum.auto()
    PRIM = enum.auto()
    PTR = enum.auto()
    REF = enum.auto()
    RV_REF = enum.auto()
    ARR = enum.auto()
    FUN = enum.auto()
    STRUCT = enum.auto()
    MACRO = enum.auto()
    ALIAS = enum.auto()
    NAMESPACE = enum.auto()
    GENERIC = enum.auto()


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

    def __init__(self, ckind: VariableCompKind, elem_ckind: VariableCompKind = VariableCompKind(VariableKind.INT64, VariableMetaKind.PRIM), name: str = '') -> None:
        self.name = name
        self.ckind = ckind
        self.elem_ckind = elem_ckind

    def __eq__(self, other):
        if isinstance(other, VariableType):
            return (self.ckind, self.elem_ckind, self.name) == (other.ckind, other.elem_ckind, other.name)
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


@dataclass
class ParsedType:
    """
    Used by the parser to store type information
    """
    var_type: VariableType
    elem_type: VariableType
    elem_cnt: int


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


class PointerType(enum.Enum):
    PTR = enum.auto()
    REF = enum.auto()
    RV_REF = enum.auto()


class Pointer:
    """
    Contains the meta-data of a pointer type.
    """

    def __init__(self, name: str, elem_cnt: int, elem_type: VariableType, off: int, ptr_type: PointerType, is_local: bool = False, value: int = 0):
        self.name = name
        self.elem_cnt = elem_cnt
        self.elem_type = elem_type
        self.off = off
        self.ptr_type = ptr_type
        self.is_local = is_local
        self.value = value


@dataclass
class Array:
    """
    Contains the meta-data of an array type.
    """

    name: str
    elem_cnt: int
    elem_type: VariableType
    off: int
    is_local: bool


@dataclass
class Structure:
    name: str
    vtype: VariableType
    elem_names: List[str]
    elem_types: List[VariableType]


@dataclass
class FunctionSignature:
    name: str
    arg_cnt: int
    arg_names: List[str]
    arg_types: List[VariableType]
    ret_type: VariableType
    is_extern: bool
    is_generic: bool
    parser: Any


@dataclass
class Function:
    """
    Contains the meta-data of a function type.
    """
    # Possible generic function
    # Template type -> arg_type
    # gen_types: List[int] (generic-id's)
    # FUN_CALL -> signatures: List[List[VariableType]] -> fun_X()

    name: str
    arg_cnt: int
    arg_names: List[str]
    arg_types: List[VariableType]
    ret_type: VariableType
    off: int
    is_variadic: bool
    is_extern: bool
    signatures: List[FunctionSignature]


@dataclass
class MacroSignature:
    arg_cnt: int
    arg_names: List[str]
    parser: Any


@dataclass
class Macro:
    name: str
    arg_cnt: int
    signatures: List[MacroSignature]


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
    OP_OR = enum.auto()
    OP_AND = enum.auto()
    OP_BIT_OR = enum.auto()
    OP_BIT_AND = enum.auto()
    OP_ASSIGN = enum.auto()
    DECLARATION = enum.auto()
    ARR_DECL = enum.auto()
    STRUCT = enum.auto()
    STRUCT_DECL = enum.auto()
    STRUCT_ARR_DECL = enum.auto()
    STRUCT_ELEM_DECL = enum.auto()
    OP_GT = enum.auto()
    OP_LT = enum.auto()
    OP_LTE = enum.auto()
    OP_GTE = enum.auto()
    OP_EQ = enum.auto()
    OP_NEQ = enum.auto()
    TERN = enum.auto()
    TERN_COND = enum.auto()
    TERN_BODY = enum.auto
    IF = enum.auto()
    ELIF = enum.auto()
    ELSE = enum.auto()
    FOR = enum.auto()
    WHILE = enum.auto()
    GLUE = enum.auto()
    FUN = enum.auto()
    FUN_CALL = enum.auto()
    CHAR_LIT = enum.auto()
    TRUE_LIT = enum.auto()
    FALSE_LIT = enum.auto()
    OP_WIDEN = enum.auto()
    RET = enum.auto()
    ARR_ACC = enum.auto()
    ELEM_ACC = enum.auto()
    REF = enum.auto()
    DEREF = enum.auto()
    STR_LIT = enum.auto()
    DEFER = enum.auto()
    ASM = enum.auto()
    CAST = enum.auto()
    STRFY = enum.auto()
    MOVE = enum.auto()
    TYPE = enum.auto()
    OFF = enum.auto()
    LEN = enum.auto()
    LIT = enum.auto()
    SIZE = enum.auto()
    COUNT = enum.auto()
    BLOCK = enum.auto()
    NAMESPACE = enum.auto()
    END = enum.auto()


class Node:
    """
    Represents a node of the AST (operation).
    """

    def __init__(self, kind: NodeKind, ntype: VariableType, value: str, left: Optional[Node] = None, right: Optional[Node] = None, middle: Optional[Node] = None):
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


class GenBase:
    def gen(self, node: Node):
        raise NotImplementedError(''.join(['GenBase acts as an abstract class',
                                           'Inherit it and provide a custom gen implementation']))


def color_str(color: Color, msg: str):
    if not color_enabled:
        return msg
    return f'{color}{msg}{Color.ENDC}'


#! Warning: Relies on parser state-related variables.
def print_error(loc: str, msg: str, parser=None, node=None):
    line = ('' if parser is None or parser.no_more_lines() else '\"' +
            parser.curr_line().lstrip('\t ').rstrip('\n') + '\"')
    desc = color_str(Color.FAIL, f'{loc}: {msg}')
    print(file=sys.stderr)
    print_stack(file=sys.stderr)
    print(file=sys.stderr)
    if parser is not None:
        print(f'location: {color_str(Color.FAIL, line)}', file=sys.stderr)
        print(f'{parser.source}:{parser.lines_idx}:{parser.tokens_idx}: {desc}',
              file=sys.stderr)
    else:
        from GenStr import tree_str
        print(f'location: {color_str(Color.FAIL, tree_str(node))}',
              file=sys.stderr)
        print(f'ERROR: {desc}', file=sys.stderr)
    exit(1)


def print_warning(loc: str, msg: str, parser=None, node=None):
    line = ('' if parser is None or parser.no_more_lines() else '\"' +
            parser.curr_line().lstrip('\t ').rstrip('\n') + '\"')
    desc = color_str(Color.WARNING, f'WARNING: {loc}: {msg}')
    if parser is not None:
        print(f'location: {color_str(Color.WARNING, line)}', file=sys.stderr)
        print(f'{parser.source}:{parser.lines_idx}:{parser.tokens_idx}: {desc}',
              file=sys.stderr)
    else:
        from GenStr import tree_str
        print(f'location: {color_str(Color.FAIL, tree_str(node))}',
              file=sys.stderr)
        print(desc, file=sys.stderr)
    print(file=sys.stderr)


def print_stdout(msg: str = ''):
    print(msg, file=stdout)


def check_ident(name: str, meta_kind: Optional[VariableMetaKind] = None, use_mkind: bool = False):
    if name not in ident_map:
        return

    meta_kind2 = ident_map.get(name)
    if use_mkind and meta_kind != meta_kind2:
        if meta_kind is None:
            print_error('check_ident',
                        f'Redefinition of identifier {name}, (meta_kind = {meta_kind2})')
        else:
            print_error('check_ident',
                        f'Redefinition of identifier {name}, (meta_kind = {meta_kind}, meta_kind2 = {meta_kind2})')


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


def full_name_of_fun(name: str, force_global: bool = False, exhaustive_match: bool = True):
    # Namespace match
    global_name = "_".join(module_name_list + [name])
    if force_global or global_name in fun_map:
        return global_name

    if exhaustive_match:
        list_cpy = list(module_name_list)
        while len(list_cpy) > 0:
            new_name = '_'.join(list_cpy + [name])
            if new_name in ident_map and ident_map.get(new_name) in (VariableMetaKind.FUN, VariableMetaKind.MACRO):
                return new_name

            list_cpy.pop()

        # print_error('full_name_of_fun',
        #             f'Exhaustive match for {name} failed')

    # Direct match (guess)
    return name


def full_name_of_var(name: str, force_local: bool = False, exhaustive_match: bool = True):
    # def exists(name: str):
    #     return name in ident_map and ident_map.get(name) != VariableMetaKind.STRUCT

    # Local match (forced)
    if force_local:
        return "_".join(module_name_list + fun_name_list + [name])

    # Namespace match
    global_name = "_".join(module_name_list + [name])
    if global_name in ident_map:
        return global_name

    # Direct match
    if name in ident_map:
        return name

    # Exhaustive match
    if exhaustive_match:
        list_cpy = list(fun_name_list)
        while len(list_cpy) > 0:
            new_name = '_'.join(list_cpy + [name])
            if new_name in ident_map and ident_map.get(new_name) not in (VariableMetaKind.FUN, VariableMetaKind.MACRO):
                return new_name

            list_cpy.pop()

        # print_error('full_name_of_var',
        #             f'Exhaustive match for {name} failed')

    # Local match (guess)
    return "_".join(fun_name_list + [name])


def off_of(ident: str) -> int:
    if ident not in ident_map:
        print_error('off_of', f'No such identifier {ident}')

    meta_kind = ident_map.get(ident)

    if meta_kind in (VariableMetaKind.PRIM, VariableMetaKind.BOOL):
        return var_map.get(ident).off

    if meta_kind == VariableMetaKind.ARR:
        return arr_map.get(ident).off

    if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF, VariableMetaKind.RV_REF):
        return ptr_map.get(ident).off

    print_error(
        'off_of', f'No such meta kind {meta_kind} for identifier {ident}')


# Parses the type of the identifier
def type_of(sym: str) -> VariableType:
    if sym not in type_map:
        print_error('type_of', f'Invalid type identifier {sym}')

    return type_map.get(sym)


def type_of_cast(sym: str) -> VariableType:
    if sym.endswith("&"):
        return VariableType(ref_ckind, type_of(sym[:-1]).ckind)

    if sym.endswith("*"):
        return VariableType(ptr_ckind, type_of(sym[:-1]).ckind)

    return type_of(sym)


def rev_type_of_ident(name: str) -> str:
    rev_kind_map = {
        VariableKind.INT64: 'int64',
        VariableKind.INT32: 'int32',
        VariableKind.INT16: 'int16',
        VariableKind.INT8: 'int8',
        VariableKind.VOID: 'void',
    }

    def rev_of(ckind: VariableCompKind, name: str = None):
        if name:
            return name

        if ckind == bool_ckind:
            return 'bool'

        return rev_kind_map.get(ckind.kind)

    if name not in ident_map:
        print_error('rev_type_of_ident', f'No such identifier {name}')

    meta_kind = ident_map.get(name)
    if meta_kind == VariableMetaKind.GENERIC:
        return rev_type_of(any_type)

    if meta_kind == VariableMetaKind.ANY:
        return rev_type_of(any_type)

    if meta_kind in (VariableMetaKind.PRIM, VariableMetaKind.BOOL):
        if name not in var_map:
            print_error('rev_type_of_ident', f'No such variable {name}')

        var = var_map.get(name)
        return rev_of(var.vtype.ckind)

    if meta_kind == VariableMetaKind.ARR:
        if name not in arr_map:
            print_error('rev_type_of_ident', f'No such array {name}')

        arr = arr_map.get(name)
        return f'{rev_of(arr.elem_type.ckind)}[{arr.elem_cnt}]'

    if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF, VariableMetaKind.RV_REF):
        if name not in ptr_map:
            print_error('rev_type_of_ident', f'No such pointer {name}')

        ptr = ptr_map.get(name)
        specifier = ''
        if ptr.ptr_type == PointerType.REF:
            specifier = '&'
        elif ptr.ptr_type == PointerType.RV_REF:
            specifier = '&&'
        elif ptr.elem_cnt == 0:
            specifier = '*'
        else:
            specifier = f'[{ptr.elem_cnt}]*'
        return f'{rev_of(ptr.elem_type.ckind, ptr.elem_type.name)}{specifier}'

    print_error('rev_type_of_ident', f'No such meta kind {meta_kind}')


def rev_type_of(vtype: VariableType) -> str:
    rev_kind_map = {
        VariableKind.INT64: 'int64',
        VariableKind.INT32: 'int32',
        VariableKind.INT16: 'int16',
        VariableKind.INT8: 'int8',
        VariableKind.VOID: 'void',
    }

    def rev_of(ckind: VariableCompKind):
        if ckind == any_ckind:
            return 'any'
        if ckind == bool_ckind:
            return 'bool'

        return rev_kind_map.get(ckind.kind)

    if vtype.kind() not in rev_kind_map:
        print_error('rev_type_of', f'Invalid variable kind {vtype.kind}')

    if vtype.ckind == struct_ckind:
        return vtype.name

    if vtype in (any_type, bool_type):
        return rev_of(vtype.ckind)

    if vtype.ckind == rv_ref_ckind:
        if vtype.elem_ckind == struct_ckind:
            return f'{vtype.name}&&'
        else:
            return f'{rev_of(vtype.elem_ckind)}&&'

    if vtype.ckind == ref_ckind:
        if vtype.elem_ckind == struct_ckind:
            return f'{vtype.name}&'
        else:
            return f'{rev_of(vtype.elem_ckind)}&'

    if vtype.ckind == ptr_ckind:
        if vtype.elem_ckind == struct_ckind:
            return f'{vtype.name}*'
        else:
            return f'{rev_of(vtype.elem_ckind)}*'

    if vtype.ckind == arr_ckind:
        return f'{rev_of(vtype.elem_ckind)}[]'

    return rev_of(vtype.ckind)


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
        # print_error('type_of_ident', f'No such identifier {ident}')
        return any_type

    meta_kind = ident_map.get(ident)

    if meta_kind == VariableMetaKind.FUN:
        return VariableType(VariableCompKind(VariableKind.INT64, VariableMetaKind.FUN), name=ident)

    if meta_kind == VariableMetaKind.NAMESPACE:
        return void_type

    if meta_kind == VariableMetaKind.GENERIC:
        return any_type

    if meta_kind == VariableMetaKind.ANY:
        return any_type

    if meta_kind == VariableMetaKind.STRUCT:
        if ident not in struct_map:
            print_error('type_of_ident', f'No such struct {ident}')

        return struct_map.get(ident).vtype

    if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF, VariableMetaKind.RV_REF):
        if ident not in ptr_map:
            print_error('type_of_ident', f'No such variable {ident}')

        ptr = ptr_map.get(ident)
        ckind = ptr_ckind if meta_kind == VariableMetaKind.PTR else (
            ref_ckind if meta_kind == VariableMetaKind.REF else rv_ref_ckind)
        return VariableType(ckind, ptr.elem_type.ckind, ptr.elem_type.name)

    if meta_kind == VariableMetaKind.ARR:
        if ident not in arr_map:
            print_error('type_of_ident', f'No such variable {ident}')

        return VariableType(arr_ckind, arr_map.get(ident).elem_type.ckind)

    if meta_kind in (VariableMetaKind.PRIM, VariableMetaKind.BOOL):
        if ident not in var_map:
            print_error('type_of_ident', f'No such variable {ident}')

        return var_map.get(ident).vtype

    print_error('type_of_ident', f'No such meta kind {meta_kind}')


def type_of_lit(kind: NodeKind) -> VariableType:
    if kind in (NodeKind.TRUE_LIT, NodeKind.FALSE_LIT):
        return bool_type

    lit_type_map = {
        NodeKind.STR_LIT: ptr_ckind,
        NodeKind.INT_LIT: default_ckind,
        NodeKind.CHAR_LIT: VariableCompKind(VariableKind.INT8, VariableMetaKind.PRIM),
    }

    if kind not in lit_type_map:
        print_error('type_of_lit', f'Invalid node kind {kind}')

    char_ckind = VariableCompKind(VariableKind.INT8, VariableMetaKind.PRIM)
    elem_ckind = char_ckind if kind == NodeKind.STR_LIT else default_ckind
    return VariableType(lit_type_map.get(kind), elem_ckind)


def type_of_op(kind: NodeKind, prev_type: Optional[VariableType] = None) -> VariableType:
    if kind in (NodeKind.ELEM_ACC, NodeKind.TERN_COND, NodeKind.TERN_BODY):
        return prev_type

    if kind == NodeKind.ARR_ACC:
        return VariableType(prev_type.elem_ckind, name=prev_type.name)

    if kind == NodeKind.REF:
        if prev_type.ckind == ref_ckind:
            return VariableType(ptr_ckind, prev_type.elem_ckind, name=prev_type.name)
        else:
            return VariableType(ptr_ckind, prev_type.ckind, name=prev_type.name)

    if kind == NodeKind.DEREF:
        # Boolean fix
        if prev_type.elem_ckind == bool_ckind:
            return bool_type

        return VariableType(prev_type.elem_ckind, name=prev_type.name)

    ckind_map = {
        NodeKind.CAST: default_ckind,
        NodeKind.OP_MULT: default_ckind,
        NodeKind.OP_ADD: default_ckind,
        NodeKind.OP_SUB: default_ckind,
        NodeKind.OP_DIV: default_ckind,
        NodeKind.OP_MOD: default_ckind,
        NodeKind.OP_AND: bool_ckind,
        NodeKind.OP_OR: bool_ckind,
        NodeKind.OP_BIT_OR: default_ckind,
        NodeKind.OP_BIT_AND: default_ckind,
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
        # NodeKind.FUN_CALL: default_ckind,
        NodeKind.OP_ASSIGN: default_ckind,
        # NodeKind.ARR_ACC: default_ckind
    }

    if kind not in ckind_map:
        print_error('type_of_op', f'Invalid node kind {kind}')

    return VariableType(ckind_map.get(kind), default_ckind)


def type_compatible(kind: NodeKind, ckind: VariableCompKind, ckind2: VariableCompKind, ref_is_ptr: bool = True) -> bool:
    if ckind == any_ckind or ckind2 == any_ckind:
        return True

    if kind in (
            NodeKind.STRUCT_ELEM_DECL,
            NodeKind.DECLARATION,
            NodeKind.ARR_DECL,
            NodeKind.ELEM_ACC,
            NodeKind.ARR_ACC,
            NodeKind.WHILE,
            NodeKind.IF):
        return True

    if ckind == ckind2:
        return True

    if kind != NodeKind.GLUE and (ckind == void_ckind or ckind2 == void_ckind):
        return False

    if ckind.meta_kind == ckind2.meta_kind:
        return True

    if ckind == any_ckind or ckind2 == any_ckind:
        return True

    if ckind in (ptr_ckind, ref_ckind) and ckind2 in (ptr_ckind, ref_ckind) and ref_is_ptr:
        return True

    if kind == NodeKind.FUN_CALL and ckind == arr_ckind and ckind2 == ptr_ckind:
        return True

    if kind == NodeKind.OP_ASSIGN and ckind == ptr_ckind and ckind2 == arr_ckind:
        return True

    if kind == NodeKind.TERN_COND and ckind2 == bool_ckind:
        return True

    return False


def allowed_op(ckind: VariableCompKind):
    # Fix for macros
    if ckind == any_ckind:
        return [
            NodeKind.TERN_COND,
            NodeKind.TERN_BODY,
            NodeKind.ELEM_ACC,
            NodeKind.IDENT,
            NodeKind.INT_LIT,
            NodeKind.OP_ADD,
            NodeKind.OP_SUB,
            NodeKind.OP_MULT,
            NodeKind.OP_DIV,
            NodeKind.OP_MOD,
            NodeKind.OP_AND,
            NodeKind.OP_OR,
            NodeKind.OP_BIT_OR,
            NodeKind.OP_BIT_AND,
            NodeKind.OP_ASSIGN,
            NodeKind.DECLARATION,
            NodeKind.OP_GT,
            NodeKind.OP_LT,
            NodeKind.OP_LTE,
            NodeKind.OP_GTE,
            NodeKind.OP_EQ,
            NodeKind.OP_NEQ,
            NodeKind.IF,
            NodeKind.WHILE,
            NodeKind.GLUE,
            NodeKind.FUN,
            NodeKind.FUN_CALL,
            NodeKind.CHAR_LIT,
            NodeKind.TRUE_LIT,
            NodeKind.FALSE_LIT,
            NodeKind.OP_WIDEN,
            NodeKind.RET,
            NodeKind.ARR_ACC,
            NodeKind.ELEM_ACC,
            NodeKind.REF,
            NodeKind.DEREF,
            NodeKind.STR_LIT,
            NodeKind.DEFER,
            NodeKind.ASM,
            NodeKind.CAST
        ]

    if ckind.meta_kind == VariableMetaKind.PRIM:
        return [
            NodeKind.TERN_COND,
            NodeKind.TERN_BODY,
            NodeKind.INT_LIT,
            NodeKind.CHAR_LIT,
            NodeKind.CAST,
            NodeKind.OP_ADD,
            NodeKind.OP_SUB,
            NodeKind.OP_MULT,
            NodeKind.OP_DIV,
            NodeKind.OP_MOD,
            NodeKind.OP_BIT_AND,
            NodeKind.OP_BIT_OR,
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

    if ckind == bool_ckind:
        return [
            NodeKind.TERN_COND,
            NodeKind.TERN_BODY,
            NodeKind.TRUE_LIT,
            NodeKind.FALSE_LIT,
            NodeKind.CAST,
            NodeKind.OP_ASSIGN,
            NodeKind.OP_GT,
            NodeKind.OP_LT,
            NodeKind.OP_OR,
            NodeKind.OP_AND,
            NodeKind.OP_LTE,
            NodeKind.OP_GTE,
            NodeKind.OP_EQ,
            NodeKind.OP_NEQ,
            NodeKind.GLUE,
            NodeKind.REF,
        ]

    if ckind == void_ckind:
        return [
            NodeKind.ELEM_ACC,
            NodeKind.CAST,
            NodeKind.GLUE
        ]

    if ckind == arr_ckind:
        return [
            NodeKind.TERN_COND,
            NodeKind.TERN_BODY,
            NodeKind.CAST,
            NodeKind.OP_ADD,
            NodeKind.OP_SUB,
            NodeKind.DEREF,
            NodeKind.ARR_ACC,
            NodeKind.GLUE,
            NodeKind.REF
        ]

    if ckind == ptr_ckind:
        return [
            NodeKind.TERN_COND,
            NodeKind.TERN_BODY,
            NodeKind.CAST,
            NodeKind.GLUE,
            NodeKind.ARR_ACC,
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

    if ckind in (ref_ckind, rv_ref_ckind):
        return [
            NodeKind.TERN_COND,
            NodeKind.TERN_BODY,
            NodeKind.CAST,
            NodeKind.GLUE,
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
            NodeKind.ELEM_ACC,
            NodeKind.REF
        ]

    if ckind == struct_ckind:
        return [
            NodeKind.TERN_COND,
            NodeKind.TERN_BODY,
            NodeKind.OP_ASSIGN,
            NodeKind.ELEM_ACC,
            NodeKind.REF
        ]

    if ckind == fun_ckind:
        return [
            NodeKind.TERN_COND,
            NodeKind.TERN_BODY,
            NodeKind.OP_ASSIGN,
            NodeKind.REF
        ]

    print_error('allowed_op', f'Invalid type: {ckind}')


def needs_widen(ckind: VariableCompKind, ckind2: VariableCompKind):
    if ckind == ckind2:
        return 0

    if ckind == struct_ckind or ckind2 == struct_ckind:
        return 0

    if ckind == struct_ckind or ckind2 == struct_ckind:
        return 0

    if ckind == any_ckind or ckind2 == any_ckind:
        return 0

    if ckind == ref_ckind or ckind2 == ref_ckind:
        return 0

    if ckind == ptr_ckind or ckind2 == ptr_ckind:
        return 0

    if ckind == arr_ckind or ckind2 == arr_ckind:
        return 0

    if ckind == void_ckind or ckind2 == void_ckind:
        return 0

    meta_kinds = (VariableMetaKind.PRIM, VariableMetaKind.BOOL)
    if ckind.meta_kind in meta_kinds and ckind2.meta_kind in meta_kinds:
        if ckind.kind == ckind2.kind:
            return 0

        return (2 if cmp_var_kind(ckind.kind, ckind2.kind) else 1)

    print_error('needs_widen', f'Invalid composite kinds ({ckind, ckind2})')


def elem_count_of(ident: str) -> int:
    if ident not in ident_map:
        print_error('size_of_ident', f'No such identifier {ident}')

    meta_kind = ident_map.get(ident)

    if meta_kind == VariableMetaKind.ARR:
        arr = arr_map.get(ident)
        return arr.elem_cnt

    if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF):
        ptr = ptr_map.get(ident)
        return 1 if ptr.elem_cnt == 0 else ptr.elem_cnt

    return 1


def size_of(ckind: VariableCompKind) -> int:
    #! BUG: Should be corrected later
    if ckind == struct_ckind:
        return 0

    if ckind == bool_ckind:
        return 1

    if ckind in (gen_ckind, any_ckind, ptr_ckind, ref_ckind, rv_ref_ckind, arr_ckind):
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


def is_local_ident(ident: str) -> bool:
    if ident not in ident_map:
        print_error('is_local_ident', f'No such identifier {ident}')

    meta_kind = ident_map.get(ident)
    if meta_kind in (VariableMetaKind.PRIM, VariableMetaKind.BOOL):
        return var_map.get(ident).is_local

    if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF):
        return ptr_map.get(ident).is_local

    if meta_kind == VariableMetaKind.ARR:
        return arr_map.get(ident).is_local

    print_error('is_local_ident', f'No such meta kind {meta_kind}')


def size_of_ident(ident: str) -> int:
    if ident not in ident_map:
        print_error('size_of_ident', f'No such identifier {ident}')

    meta_kind = ident_map.get(ident)

    if meta_kind in (VariableMetaKind.PRIM, VariableMetaKind.BOOL):
        return size_of(var_map.get(ident).vtype.ckind)

    if meta_kind == VariableMetaKind.ARR:
        arr = arr_map.get(ident)
        return size_of(arr.elem_type.ckind) * arr.elem_cnt

    if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF):
        ptr = ptr_map.get(ident)
        return size_of(ptr_ckind) if ptr.elem_cnt == 0 else size_of(ptr.elem_type.ckind) * ptr.elem_cnt

    print_error('size_of_ident', f'No such meta kind {meta_kind}')


def arg_cnt(node: Node) -> int:
    arg_cnt = 0
    while node is not None:
        arg_cnt += 1
        node = node.left

    return arg_cnt


def args_to_list(node: Node) -> List[Node]:
    if node is None:
        return []

    glue_node = node
    arg_list: list[Node] = []
    if glue_node.kind != NodeKind.GLUE:
        arg_list.append(glue_node)
    else:
        while glue_node is not None and glue_node.kind == NodeKind.GLUE:
            arg_list.append(glue_node.right)
            glue_node = glue_node.left

        arg_list.reverse()

    return arg_list


def gen_compatible(sig: FunctionSignature, arg_types: List[VariableType]):
    gen_map = dict()
    for arg_type, sig_arg_type in zip(arg_types, sig.arg_types):
        if sig_arg_type.ckind == gen_ckind:
            gen_name = sig.name
            gen_type = gen_map.get(gen_name)

            if gen_type and gen_type != arg_type:
                return False

            gen_map[gen_name] = arg_type

    return True


def _find_signature(fun: Function, arg_types: List[VariableType], check_len: bool = True, check_refs: bool = False) -> Optional[FunctionSignature]:
    cnt = 0
    sig = None

    def is_generic(sig: FunctionSignature):
        return sig.is_generic

    def matches_ref(arg_type: VariableType, sig_arg_type: VariableType):
        return ref_of(arg_type) == sig_arg_type

    # Looks for an exact match
    for signature in fun.signatures:
        if not is_generic(signature) and arg_types == signature.arg_types:
            return signature

    # Looks for a generic match
    for signature in fun.signatures:
        if is_generic(signature) and gen_compatible(signature, arg_types):
            cnt = cnt + 1
            sig = signature

    # Ensures that only one generic match is valid
    if cnt == 1:
        return sig
    elif cnt > 0:
        print_error("_find_signature",
                    f"Multiple matches found for function {fun.name}")

    # Looks for compatible matches
    for signature in fun.signatures:
        if not is_generic(signature) and (fun.is_variadic or not check_len or len(arg_types) == signature.arg_cnt):
            compatible = True
            for arg_type, fun_arg_type in zip(arg_types, signature.arg_types):
                if not (type_compatible(NodeKind.FUN_CALL, arg_type.ckind, fun_arg_type.ckind) or (check_refs and matches_ref(arg_type, fun_arg_type))) or (arg_type.name != fun_arg_type.name and arg_type != any_type and fun_arg_type != any_type):
                    compatible = False
                    break

            if compatible:
                return signature

    return None


def find_signature(fun: Function, node: Node) -> Optional[FunctionSignature]:
    def get_type(node: Node) -> VariableType:
        return node.ntype

    args = args_to_list(node)
    if None in args:
        for arg in args:
            print(rev_type_of(arg.ntype) if arg else 'None', end=' ')

    arg_types = list(map(get_type, args))
    return _find_signature(fun, arg_types)


# Checks if signature already exists
def check_signature(fun: Function, sig: FunctionSignature) -> bool:
    for signature in fun.signatures:
        if sig.arg_types == signature.arg_types:
            return True

    return False


def ref_of(vtype: VariableType) -> VariableType:
    return VariableType(ref_ckind, vtype.ckind, vtype.name)


def rv_ref_of(vtype: VariableType) -> VariableType:
    return VariableType(rv_ref_ckind, vtype.ckind, vtype.name)


def ptr_type_of(meta_kind: VariableMetaKind):
    if meta_kind == VariableMetaKind.PTR:
        return PointerType.PTR
    if meta_kind == VariableMetaKind.REF:
        return PointerType.REF
    if meta_kind == VariableMetaKind.RV_REF:
        return PointerType.RV_REF

    print_error('ptr_type_of', f'Invalid meta kind {meta_kind}')


def ref_node(node: Node) -> Node:
    return Node(NodeKind.REF, ref_of(node.ntype), '&', node)


def compute_signature(name: str, arg_types: List[VariableType]):
    return '_'.join([name] + list(map(rev_type_of, arg_types)) + ([str(len(arg_types))] if len(arg_types) > 0 else [])).replace(
        '*', 'ptr').replace('&', 'ref')


def glue_statements(node_list: List[Optional[Node]], in_call: bool = False) -> Optional[Node]:
    if len(node_list) == 0:
        return None

    glue_node = None
    for node in node_list:
        if node is None:
            continue

        if glue_node is None:
            glue_node = node
        else:
            if glue_node.kind != NodeKind.GLUE and in_call:
                glue_node = Node(NodeKind.GLUE, void_type, '', Node(
                    NodeKind.GLUE, void_type, '', None, glue_node), node)
            else:
                glue_node = Node(NodeKind.GLUE, void_type, '', glue_node, node)

    return glue_node


def to_predeferred(node: Node):
    global predeferred
    if not predeferred:
        predeferred = node
    else:
        predeferred = glue_statements([predeferred, node])


def node_is_cmp(kind: NodeKind) -> bool:
    return kind in (
        NodeKind.OP_EQ,
        NodeKind.OP_NEQ,
        NodeKind.OP_GT,
        NodeKind.OP_LT,
        NodeKind.OP_GTE,
        NodeKind.OP_LTE
    )


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


def get_counter():
    global counter
    counter += 1
    return counter


REG_TABLE = (
    ('%rbx', '%ebx', '%bx', '%bl'),
    ('%rcx', '%ecx', '%cx', '%cl'),
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
    ('%rax', '%eax', '%ax', '%al'),
    ('%rdx', '%edx', '%dx', '%dl'),
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

BOOL_VALUES = {
    "true": "1",
    "false": "0"
}

# Configuration flag
color_enabled = True
comments_enabled = True
stdout = sys.stdout


counter = 0
var_off = 0
block_cnt = 0
macro_map: Dict[str, Macro] = dict()
var_map: Dict[str, Variable] = dict()
fun_map: Dict[str, Function] = dict()
struct_map: Dict[str, Structure] = dict()
# Redirects overloads to original function name
fun_sig_map: Dict[str, str] = dict()
arr_map: Dict[str, Array] = dict()
ptr_map: Dict[str, Pointer] = dict()
alias_map: Dict[str, str] = dict()
ident_map: Dict[str, VariableMetaKind] = dict()
str_lit_map: Dict[str, str] = dict()
opd_map = {reg: None for reg in REGS}
reg_avail_map = {reg: True for reg in REGS}
fun_name_list: List[str] = []
module_name_list: List[str] = []
ptr_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.PTR)
ref_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.REF)
rv_ref_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.RV_REF)
arr_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.ARR)
void_ckind = VariableCompKind(VariableKind.VOID, VariableMetaKind.PRIM)
bool_ckind = VariableCompKind(VariableKind.INT8, VariableMetaKind.BOOL)
default_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.PRIM)
fun_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.FUN)
any_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.ANY)
struct_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.STRUCT)
gen_ckind = VariableCompKind(VariableKind.INT64, VariableMetaKind.GENERIC)
void_type = VariableType(void_ckind)
bool_type = VariableType(bool_ckind)
default_type = VariableType(default_ckind)
any_type = VariableType(any_ckind)
struct_type = VariableType(struct_ckind)
str_type = VariableType(ptr_ckind, VariableCompKind(
    VariableKind.INT8, VariableMetaKind.PRIM))
fun_name = ''
macro_name = ''
struct_name = ''
fun_has_ret = False
fun_ret_type = void_type
returned: list[str] = []
included: set[str] = set()
include_list: list[str] = []
macro_arg_cnt = 0
fun_gen_map: Dict[str, VariableType] = dict()
macro_arg_map: Dict[str, Node] = dict()
deferred: Optional[Node] = None
predeferred: Optional[Node] = None
hoisted: Optional[Node] = None

type_map = {
    'bool': bool_type,
    'int64': default_type,
    'int32': VariableType(VariableCompKind(VariableKind.INT32, VariableMetaKind.PRIM)),
    'int16': VariableType(VariableCompKind(VariableKind.INT16, VariableMetaKind.PRIM)),
    'int8': VariableType(VariableCompKind(VariableKind.INT8, VariableMetaKind.PRIM)),
    'void': VariableType(VariableCompKind(VariableKind.VOID, VariableMetaKind.PRIM)),
}
