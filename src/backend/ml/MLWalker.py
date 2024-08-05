import Def
from Def import Node
from Def import NodeKind
from Def import Color
from Def import color_str
from Def import rev_type_of
from Def import rev_type_of_ident
from Def import print_error

from backend.Walker import Walker
from backend.Walker import fun_call_tree_str


def ml_walker_step(node: Node, parent: Node, left, right, middle, indent_cnt: int):

    if node is None:
        return ''

    indent = '  ' * indent_cnt

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
    if node.kind == NodeKind.OP_ASSIGN:
        return f'({left} = {right})'
    if node.kind == NodeKind.DECLARATION:
        return f'{color_str(Color.BLUE, "let")} {node.left.value}: {rev_type_of_ident(node.left.value)} = {right}'
    if node.kind == NodeKind.ARR_DECL:
        return f'{color_str(Color.BLUE, "let")} {node.value}: {rev_type_of_ident(node.value)}'
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
            return f'{color_str(Color.BLUE, "if")} {middle}\n  {indent + left}\n{indent}{color_str(Color.BLUE, "else")}\n  {indent + right}'
        else:
            return f'{color_str(Color.BLUE, "if")} {middle}\n  {indent + left}'

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
        return f'{node.value}({fun_call_tree_str(node, ml_walk)})'
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

    print_error('ml_walker_step', f'Invalid node kind {node.kind}')


def ml_walk(node: Node) -> str:
    walker = Walker(ml_walker_step)
    return walker.walk(node)
