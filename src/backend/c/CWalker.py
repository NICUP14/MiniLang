import Def
from Def import Node
from Def import NodeKind
from Def import Color
from Def import color_str
from Def import print_error
from Def import find_signature

from backend.c.CDef import has_semicolon
from backend.c.CDef import c_rev_type_of
from backend.c.CDef import c_rev_type_of_ident
from backend.c.CDef import c_expand_builtin
from backend.Walker import Walker
from backend.Walker import fun_call_tree_str


def c_walker_step(node: Node, parent: Node, left, right, middle, indent_cnt: int):
    if node is None:
        return ''

    indent = '  ' * indent_cnt
    prev_indent = '  ' * (indent_cnt - 1)
    add_left_semi = node.left is not None and has_semicolon(node.left.kind)
    add_right_semi = node.right is not None and has_semicolon(node.right.kind)

    if node.kind in (NodeKind.INT_LIT, NodeKind.CHAR_LIT):
        return node.value
    if node.kind in (NodeKind.TRUE_LIT, NodeKind.FALSE_LIT):
        return color_str(Color.BLUE, node.value)
    if node.kind == NodeKind.STR_LIT:
        string = node.value.replace('\n', '\\n').replace(
            '\t', '\\t').replace('\\end', 'end')
        return string
    if node.kind == NodeKind.IDENT:
        if Def.ident_map.get(node.value) == Def.VariableMetaKind.REF and (
                parent is None or parent.kind not in (NodeKind.REF, NodeKind.DECLARATION)):
            return f'*{node.value}'
        return node.value
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
    if node.kind == NodeKind.OP_BIT_AND:
        return f'({left} & {right})'
    if node.kind == NodeKind.OP_BIT_OR:
        return f'({left} | {right})'
    if node.kind == NodeKind.OP_AND:
        return f'({left} && {right})'
    if node.kind == NodeKind.OP_OR:
        return f'({left} || {right})'
    if node.kind == NodeKind.OP_ASSIGN:
        # ptr = Def.ptr_map.get(node.left.value)
        # if ptr.ref:
        #    return f'(*{left} = {right})'
        # else:
        return f'({left} = {right})'
    if node.kind == NodeKind.STRUCT:
        return f'typedef {color_str(Color.BLUE, "struct")} {"{"}\n {indent + left}'
    if node.kind == NodeKind.DECLARATION:
        return f'{color_str(Color.GREEN, c_rev_type_of_ident(node.left.value))} {left} = {right}'
    if node.kind == NodeKind.STRUCT_DECL:
        if node.right is not None:
            return f'{color_str(Color.GREEN, c_rev_type_of(node.ntype))} {left} = {right}'
        else:
            return f'{color_str(Color.GREEN, c_rev_type_of(node.ntype))} {node.value}'
    if node.kind == NodeKind.STRUCT_ELEM_DECL:
        return f'{color_str(Color.GREEN, c_rev_type_of_ident(node.left.value))} {left}'
    if node.kind == NodeKind.ARR_DECL:
        arr = Def.arr_map.get(node.value)
        return f'{color_str(Color.GREEN, c_rev_type_of(arr.elem_type))} {node.value}[{arr.elem_cnt}]'
    if node.kind == NodeKind.STRUCT_ARR_DECL:
        arr = Def.arr_map.get(node.value)
        return f'{color_str(Color.GREEN, c_rev_type_of(arr.elem_type))} {node.value}[{arr.elem_cnt}]'
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
    if node.kind == NodeKind.ELEM_ACC:
        return f'{left}.{right}'
    if node.kind == NodeKind.IF:
        # if right is not None:
        # return f'{color_str(Color.BLUE, "if")} {middle} {"{"}\n  {indent + left}{";" if add_left_semi else ""}\n{prev_indent + "}"}\n{prev_indent}{color_str(Color.BLUE, "else")} {"{"}\n{indent + right}{";" if add_right_semi else ""}'
        # else:
        return f'{color_str(Color.BLUE, "if")} {middle} {"{"}\n  {indent + left}{";" if add_left_semi else ""}'
    if node.kind == NodeKind.ELIF:
        return f'{color_str(Color.BLUE, "else if")} {middle} {"{"}\n {indent + left}{";" if add_left_semi else ""}'
    if node.kind == NodeKind.ELSE:
        return f'{color_str(Color.BLUE, "else")} {"{"}\n {indent + left}{";" if add_left_semi else ""}'
    if node.kind == NodeKind.WHILE:
        return f'{color_str(Color.BLUE, "while")} {left} {"{"}\n{right}{";" if add_right_semi else ""}'
    if node.kind == NodeKind.GLUE:
        empty_str = ''
        add_indent = parent is not None and parent.kind != NodeKind.GLUE
        if left is None:
            return f'{indent if add_indent else empty_str}{right}{";" if add_right_semi else empty_str}'
        if right is None:
            return f'{indent if add_indent else empty_str}{left}{";" if add_left_semi else empty_str}'
        else:
            return f'{indent if add_indent else empty_str}{left}{";" if add_left_semi else empty_str}\n{indent + right}{";" if add_right_semi else empty_str}'
    if node.kind == NodeKind.FUN_CALL:
        fun = Def.fun_map.get(node.value)
        sig = find_signature(fun, node.left)
        if sig is None:
            print_error('c_walker_step',
                        f'No signature of {fun.name} matches {sig}')

        return f'{sig.name}({fun_call_tree_str(node, _c_walk)})'
    if node.kind == NodeKind.ASM:
        return f'{color_str(Color.BLUE, node.value)}({node.left.value})'
    if node.kind == NodeKind.FUN:
        sig_name = node.value
        fun_name = Def.fun_sig_map.get(node.value)
        fun = Def.fun_map.get(fun_name)

        # ? Temporary
        sig = None
        for signature in fun.signatures:
            if signature.name == sig_name:
                sig = signature

        args_zip = zip(sig.arg_names, sig.arg_types)
        args_map = map(
            lambda t: f'{color_str(Color.BLUE, c_rev_type_of(t[1]))} {t[0]}', args_zip)
        args_str = ", ".join(
            list(args_map) + (['...'] if fun.is_variadic else []))
        return f'{color_str(Color.GREEN, c_rev_type_of(sig.ret_type))} {node.value}({args_str}) {"{"} \n{left}{";" if add_left_semi else ""}'
    if node.kind in (NodeKind.OP_WIDEN, NodeKind.CAST):
        return f'({color_str(Color.GREEN, c_rev_type_of(node.ntype))}){left}'
    if node.kind in (NodeKind.TYPE, NodeKind.OFF, NodeKind.LEN, NodeKind.LIT, NodeKind.SIZE, NodeKind.COUNT):
        return _c_walk(c_expand_builtin(node))
    if node.kind == NodeKind.RET:
        return f'{color_str(Color.BLUE, "return")} {left if left is not None else ""}'
    if node.kind == NodeKind.BLOCK:
        return ''
    if node.kind == NodeKind.NAMESPACE:
        return ''
    if node.kind == NodeKind.REF:
        if Def.ident_map.get(node.left.value) in (Def.VariableMetaKind.REF, Def.VariableMetaKind.ARR):
            return left
        else:
            return f'&{left}'
    if node.kind == NodeKind.DEREF:
        return f'*{left}'
    if node.kind == NodeKind.END:
        if (parent.left is not None and parent.left.kind in [
                NodeKind.NAMESPACE,
                NodeKind.BLOCK]):
            return ''
        else:
            if parent.left is not None and parent.left.kind == NodeKind.STRUCT:
                return indent + f'{"}"} {parent.left.value};\n'
            if parent.left is not None and parent.left.kind == NodeKind.FUN:
                return indent + '}\n'
            else:
                return indent + '}'

    print_error('c_walker_step', f'Invalid node kind {node.kind}')


def _c_preamble() -> str:
    headers = [
        'stdio.h',
        'stdlib.h',
        'string.h',
        'stdbool.h',
        'ctype.h'
    ]

    def include(header: str) -> str:
        return f'#include <{header}>'

    return '\n'.join(map(include, headers))


def _c_walk(node):
    walker = Walker(c_walker_step)
    return walker.walk(node)


def c_walk(node):
    return f'{_c_preamble()}\n\n{_c_walk(node)}'
