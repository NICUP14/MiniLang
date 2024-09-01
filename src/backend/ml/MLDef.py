import Def
from Def import Node
from Def import NodeKind
from Def import VariableMetaKind
from Def import default_type
from Def import arg_cnt
from Def import args_to_list
from Def import print_error
from Def import rev_type_of
from Def import rev_type_of_ident


def is_special_fun(name: str):
    return name in (
        'iter',
        'start',
        'stop',
        'next',
        'move',
        'copy',
        'destruct'
    )


def has_indent(kind: NodeKind):
    return kind in (
        NodeKind.IF,
        NodeKind.WHILE,
        NodeKind.FUN,
        NodeKind.STRUCT_DECL,
        NodeKind.BLOCK,
        NodeKind.NAMESPACE,
    )


def ml_expand_builtin(node: Node) -> Node:
    if node.kind == NodeKind.LIT:
        # Handled in MlWalker
        pass

    if node.kind == NodeKind.COUNT:
        return Node(NodeKind.INT_LIT, default_type, str(arg_cnt(node.left)))

    if node.kind == NodeKind.SIZE:
        # Handled in MlWalker
        pass

    if node.kind == NodeKind.TYPE:
        return Node(NodeKind.STR_LIT, node.ntype, f'"{rev_type_of(node.left.ntype)}"')

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

    print_error('ml_expand_builtin',
                f'Expected a builtin, got {node.kind}')
