from Parser import Node
from Parser import NodeKind
from typing import List
from typing import Tuple
from Def import rev_type_of


def has_indent(kind: NodeKind):
    return kind in (
        NodeKind.IF,
        NodeKind.WHILE,
        NodeKind.FUN,
    )


def fun_call_tree_str(node: Node):
    args = []
    glue_node = node.left

    # Fix for single-argument functions
    if glue_node.kind != NodeKind.GLUE:
        args.append(tree_str(glue_node))

    else:
        while glue_node is not None:
            args.append(tree_str(glue_node.right))
            glue_node = glue_node.left

    args.reverse()
    return ', '.join(args)


def tree_str(node: Node, parent: Node = None, cnt: int = 0):
    left = None
    right = None

    if node is None:
        return ''

    if node.kind != NodeKind.FUN_CALL and node.left:
        left = tree_str(node.left, node, cnt + has_indent(node.kind))
    if node.kind != NodeKind.FUN_CALL and node.right:
        right = tree_str(node.right, node, cnt + has_indent(node.kind))

    indent = '\t' * cnt

    if node.kind in (NodeKind.INT_LIT, NodeKind.CHAR_LIT, NodeKind.STR_LIT):
        return node.value
    if node.kind == NodeKind.IDENT:
        return f'({rev_type_of(node.ntype)})({node.value})'
    if node.kind == NodeKind.OP_ADD:
        return f'({left} + {right})'
    if node.kind == NodeKind.OP_SUB:
        return f'({left} - {right})'
    if node.kind == NodeKind.OP_DIV:
        return f'({left} / {right})'
    if node.kind == NodeKind.OP_MOD:
        return f'({left} % {right})'
    if node.kind == NodeKind.OP_MULT:
        return f'({left} * {right})'
    if node.kind == NodeKind.OP_ASSIGN:
        return f'({left} = {right})'
    if node.kind == NodeKind.OP_GT:
        return f'({left} > {right})'
    if node.kind == NodeKind.OP_LT:
        return f'({left} < {right})'
    if node.kind == NodeKind.OP_EQ:
        return f'({left} == {right})'
    if node.kind == NodeKind.OP_LTE:
        return f'({left} <= {right})'
    if node.kind == NodeKind.OP_NEQ:
        return f'({left} != {right})'
    if node.kind == NodeKind.ARR_ACC:
        return f'{left}[{right}]'
    if node.kind == NodeKind.IF:
        if right is not None:
            return f'if {tree_str(node.middle)}\n\t{indent + left}\n{indent}else\n\t{indent + right}'
        else:
            return f'if {tree_str(node.middle)}\n\t{indent + left}\n'

    if node.kind == NodeKind.WHILE:
        return f'while {left}\n{right}'
    if node.kind == NodeKind.GLUE:
        empty_str = ''
        add_indent = parent is not None and parent.kind != NodeKind.GLUE
        if right is None:
            return f'{indent if add_indent else empty_str}{left}'
        else:
            return f'{indent if add_indent else empty_str}{left}\n{indent + right}'
    if node.kind == NodeKind.FUN_CALL:
        return f'{node.value}({fun_call_tree_str(node)})'
    if node.kind == NodeKind.FUN:
        return f'fun {node.value}()\n{left}'
    if node.kind == NodeKind.OP_WIDEN:
        return f'widen({left})'
    if node.kind == NodeKind.RET:
        return f'ret {left}'
    if node.kind == NodeKind.REF:
        return f'&{left}'
    if node.kind == NodeKind.DEREF:
        return f'*{left}'

    print(f'tree_str: Invalid node kind {node.kind}')
    exit(1)
