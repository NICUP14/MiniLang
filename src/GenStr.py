import Def
from Def import Color
from Def import Node
from Def import NodeKind
from Def import color_str
from Def import rev_type_of
from Def import rev_type_of_ident
from Def import print_error


def has_indent(kind: NodeKind):
    return kind in (
        NodeKind.IF,
        NodeKind.WHILE,
        NodeKind.FUN,
        NodeKind.BLOCK,
        NodeKind.NAMESPACE
    )


def fun_call_tree_str(node: Node):
    if node.kind == NodeKind.FUN_CALL:
        name = node.value
        fun = Def.fun_map.get(name)
        if fun.arg_cnt == 0:
            return ''

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

    if node.kind == NodeKind.ARG_CNT:
        print_error('tree_str',
                    f'Use of node of kind {node.kind} (ma_arg) is not allowed outside macros')

    if node.kind != NodeKind.FUN_CALL and node.left:
        left = tree_str(node.left, node, cnt +
                        has_indent(node.kind) - (node.kind == NodeKind.END))
    if node.kind != NodeKind.FUN_CALL and node.right:
        right = tree_str(node.right, node, cnt +
                         has_indent(node.kind) - (node.kind == NodeKind.END))

    indent = '  ' * cnt

    if node.kind in (NodeKind.INT_LIT, NodeKind.CHAR_LIT):
        return node.value
    if node.kind in (NodeKind.TRUE_LIT, NodeKind.FALSE_LIT):
        return color_str(Color.BLUE, node.value)
    if node.kind == NodeKind.STR_LIT:
        string = node.value.replace('\n', '\\n').replace(
            '\t', '\\t').replace('\\end', 'end')
        return string
    if node.kind == NodeKind.IDENT:
        return f'({color_str(Color.GREEN, rev_type_of_ident(node.value))})({node.value})'
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
    if node.kind == NodeKind.OP_AND:
        return f'({left} & {right})'
    if node.kind == NodeKind.OP_OR:
        return f'({left} | {right})'
    if node.kind in (NodeKind.OP_ASSIGN, NodeKind.DECLARATION):
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
            return f'{color_str(Color.BLUE, "if")} {tree_str(node.middle)}\n  {indent + left}\n{indent}{color_str(Color.BLUE, "else")}\n  {indent + right}'
        else:
            return f'{color_str(Color.BLUE, "if")} {tree_str(node.middle)}\n  {indent + left}'

    if node.kind == NodeKind.WHILE:
        return f'{color_str(Color.BLUE, "while")} {left}\n{right}'
    if node.kind == NodeKind.GLUE:
        empty_str = ''
        add_indent = parent is not None and parent.kind != NodeKind.GLUE
        if left is None:
            return f'{indent if add_indent else empty_str}{right}'
        if right is None:
            return f'{indent if add_indent else empty_str}{left}'
        else:
            return f'{indent if add_indent else empty_str}{left}\n{indent + right}'
    if node.kind == NodeKind.FUN_CALL:
        return f'{node.value}({fun_call_tree_str(node)})'
    if node.kind == NodeKind.ASM:
        return f'{color_str(Color.BLUE, node.value)}({node.left.value})'
    if node.kind == NodeKind.FUN:
        fun = Def.fun_map.get(node.value)
        args_zip = zip(fun.arg_names, fun.arg_types)
        args_map = map(
            lambda t: f'({color_str(Color.BLUE, rev_type_of(t[1]))})({t[0]})', args_zip)
        args_str = ", ".join(
            list(args_map) + (['...'] if fun.is_variadic else []))
        return f'{color_str(Color.BLUE, "fun")} {node.value}({args_str})\n{left}'
    if node.kind == NodeKind.OP_WIDEN:
        return f'widen({left})'
    if node.kind == NodeKind.CAST:
        return f'{color_str(Color.BLUE, "cast")}(\"{color_str(Color.GREEN, rev_type_of(node.ntype))}\", {left})'
    if node.kind in (NodeKind.TYPE, NodeKind.OFF, NodeKind.LEN, NodeKind.SIZE):
        return f'{color_str(Color.BLUE, node.value)}({left})'
    if node.kind == NodeKind.RET:
        return f'{color_str(Color.BLUE, "ret")} {left}'
    if node.kind == NodeKind.BLOCK:
        return f'{color_str(Color.BLUE, "block")} {node.value}\n{left}'
    if node.kind == NodeKind.NAMESPACE:
        return f'{color_str(Color.BLUE, "namespace")} {node.value}\n{left}'
    if node.kind == NodeKind.REF:
        return f'&{left}'
    if node.kind == NodeKind.DEREF:
        return f'*{left}'
    if node.kind == NodeKind.END:
        return color_str(Color.BLUE, 'end')

    print_error('tree_str', f'Invalid node kind {node.kind}')
