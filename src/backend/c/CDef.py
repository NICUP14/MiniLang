import Def
from Def import Node
from Def import NodeKind
from Def import VariableKind
from Def import VariableMetaKind
from Def import VariableCompKind
from Def import VariableType
from Def import bool_ckind
from Def import any_ckind
from Def import ptr_ckind
from Def import arr_ckind
from Def import ref_ckind
from Def import sig_ckind
from Def import rv_ref_ckind
from Def import struct_ckind
from Def import any_type
from Def import bool_type
from Def import default_type
from Def import arg_cnt
from Def import args_to_list
from Def import print_error


def c_rev_type_of(vtype: VariableType):
    rev_kind_map = {
        VariableKind.INT64: 'int64_t',
        VariableKind.INT32: 'int32_t',
        VariableKind.INT16: 'int16_t',
        VariableKind.INT8: 'int8_t',
        VariableKind.VOID: 'void',
    }

    def rev_of(ckind: VariableCompKind):
        if ckind == any_ckind:
            return 'void*'
        if ckind == bool_ckind:
            return 'char'

        if ckind.meta_kind == VariableMetaKind.FLOAT and ckind.kind == VariableKind.INT32:
            return 'float'

        if ckind.meta_kind == VariableMetaKind.FLOAT and ckind.kind == VariableKind.INT64:
            return 'double'

        return rev_kind_map.get(ckind.kind)

    if vtype.kind() not in rev_kind_map:
        print_error('c_rev_type_of', f'Invalid variable kind {vtype.kind}')

    if vtype.ckind == sig_ckind:
        sig = Def.sig_map.get(vtype.name)
        args_str = ', '.join(map(c_rev_type_of, sig.arg_types))
        return f'{c_rev_type_of(sig.ret_type)} (*{vtype.name})({args_str})'

    if vtype.ckind == struct_ckind:
        return vtype.name

    if vtype in (any_type, bool_type):
        return rev_of(vtype.ckind)

    if vtype.ckind in (ptr_ckind, ref_ckind, rv_ref_ckind):
        if vtype.elem_ckind == struct_ckind:
            return f'{vtype.name}*'
        else:
            return f'{rev_of(vtype.elem_ckind)}*'

    if vtype.ckind == arr_ckind:
        return f'{rev_of(vtype.elem_ckind)}[]'

    return rev_of(vtype.ckind)


def c_rev_type_of_ident(name: str) -> str:
    rev_kind_map = {
        VariableKind.INT64: 'int64_t',
        VariableKind.INT32: 'int32_t',
        VariableKind.INT16: 'int16_t',
        VariableKind.INT8: 'int8_t',
        VariableKind.VOID: 'void',
    }

    def rev_of(ckind: VariableCompKind):
        if ckind == bool_ckind:
            return 'char'

        if ckind.meta_kind == VariableMetaKind.FLOAT and ckind.kind == VariableKind.INT32:
            return 'float'

        if ckind.meta_kind == VariableMetaKind.FLOAT and ckind.kind == VariableKind.INT64:
            return 'double'

        return rev_kind_map.get(ckind.kind)

    if name not in Def.ident_map:
        print_error('c_rev_type_of_ident', f'No such identifier {name}')

    meta_kind = Def.ident_map.get(name)

    if meta_kind == VariableMetaKind.STRUCT:
        return f'struct {name}'

    if meta_kind == VariableMetaKind.ANY:
        return c_rev_type_of(any_type)

    if meta_kind in (VariableMetaKind.PRIM, VariableMetaKind.FLOAT, VariableMetaKind.BOOL):
        if name not in Def.var_map:
            print_error('c_rev_type_of_ident', f'No such variable {name}')

        var = Def.var_map.get(name)
        return rev_of(var.vtype.ckind)

    if meta_kind == VariableMetaKind.ARR:
        if name not in Def.arr_map:
            print_error('c_rev_type_of_ident', f'No such array {name}')

        arr = Def.arr_map.get(name)
        return f'{rev_of(arr.elem_type.ckind)}[{arr.elem_cnt}]'

    if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF, VariableMetaKind.RV_REF):
        if name not in Def.ptr_map:
            print_error('c_rev_type_of_ident', f'No such pointer {name}')

        ptr = Def.ptr_map.get(name)
        if ptr.elem_type.ckind == struct_ckind:
            return f'{ptr.elem_type.name}*'
        else:
            return f'{rev_of(ptr.elem_type.ckind)}*'

    print_error('c_rev_type_of_ident',
                f'No such meta kind (name = {name}, meta_kind = {meta_kind})')


def is_helper_glue(parent_kind: NodeKind, kind: NodeKind):
    return parent_kind == NodeKind.GLUE and kind == NodeKind.GLUE


def is_in_block(kind: NodeKind):
    return kind in [
        NodeKind.GLUE,
        NodeKind.FUN,
        NodeKind.IF,
        NodeKind.ELIF,
        NodeKind.ELSE,
        NodeKind.END
    ]


def has_semicolon(kind: NodeKind):
    return kind not in [
        NodeKind.LIT,
        NodeKind.GLUE,
        NodeKind.FUN,
        NodeKind.IF,
        NodeKind.ELIF,
        NodeKind.ELSE,
        NodeKind.END
    ]


def c_expand_builtin(node: Node) -> Node:
    def expand_lit(node: Node):
        if node.kind == NodeKind.STR_LIT:
            return node.value.lstrip('"').rstrip('"')

        return node.value

    if node.kind == NodeKind.LIT:
        nodes = args_to_list(node.left)
        lit = ''.join(map(expand_lit, nodes))

        # ? Hacky fix
        return Node(NodeKind.INT_LIT, Def.void_type, lit)

    if node.kind == NodeKind.COUNT:
        return Node(NodeKind.INT_LIT, default_type, str(arg_cnt(node.left)))

    if node.kind == NodeKind.SIZE:
        if node.left.kind != NodeKind.IDENT:
            return Node(NodeKind.INT_LIT, default_type, 0)

        elem_cnt = Def.elem_count_of(node.left.value)
        size_str = f'(sizeof({node.left.value}) * {elem_cnt})' if elem_cnt > 1 else f'sizeof({node.left.value})'

        return Node(NodeKind.INT_LIT, default_type, size_str)

    if node.kind == NodeKind.TYPE:
        return Node(NodeKind.STR_LIT, node.ntype, f'"{c_rev_type_of(node.left.ntype)}"')

    if node.kind == NodeKind.LEN:
        if node.left.kind != NodeKind.IDENT:
            return Node(NodeKind.INT_LIT, node.ntype, '0')

        ident = node.left.value
        meta_kind = Def.ident_map.get(ident)
        if ident not in Def.ident_map:
            print_error('c_expand_builtin',
                        f'The len_of builtin only accepts pre-declared identifiers, got {ident}')

        elem_cnt = 0
        if meta_kind == VariableMetaKind.ARR:
            arr = Def.arr_map.get(ident)
            elem_cnt = arr.elem_cnt
        if meta_kind == VariableMetaKind.PTR:
            ptr = Def.ptr_map.get(ident)
            elem_cnt = ptr.elem_cnt

        return Node(NodeKind.INT_LIT, node.ntype, str(elem_cnt))

    print_error('c_expand_builtin',
                f'Expected a builtin, got {node.kind}')
