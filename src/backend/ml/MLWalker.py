import Def
from Def import Node
from Def import NodeKind
from Def import Color
from Def import color_str
from Def import print_error
from Def import find_signature
from Def import args_to_list
from Def import rev_type_of
from Def import rev_type_of_ident

from backend.Walker import Walker
from backend.Walker import fun_call_tree_str
from backend.ml.MLDef import has_indent
from backend.ml.MLDef import is_special_fun
from backend.ml.MLDef import ml_expand_builtin


def ml_walker_step(node: Node, parent: Node, left, right, middle, indent_cnt: int):
    if node is None:
        return ''

    indent = '  ' * indent_cnt
    prev_indent = '  ' * (indent_cnt - 1)

    if node.kind == NodeKind.INT_LIT:
        return color_str(Color.CYAN, node.value)
    if node.kind == NodeKind.CHAR_LIT:
        return color_str(Color.CYAN, node.value)
    if node.kind in (NodeKind.TRUE_LIT, NodeKind.FALSE_LIT):
        return color_str(Color.BLUE, node.value)
    if node.kind == NodeKind.STR_LIT:
        string = node.value.replace('\n', '\\n').replace(
            '\t', '\\t').replace('\\end', 'end')
        return color_str(Color.WARNING, string)
    if node.kind == NodeKind.IDENT:
        if Def.ident_map.get(node.value) in (Def.VariableMetaKind.REF, Def.VariableMetaKind.RV_REF) and (
                parent is None or parent.kind not in (NodeKind.REF, NodeKind.DECLARATION, NodeKind.ELEM_ACC, NodeKind.STRUCT_ELEM_DECL, NodeKind.STRUCT_ARR_DECL)):
            return f'(*{node.value})'

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
        return f'({left} = {right})'
    if node.kind == NodeKind.STRUCT:
        return f'{color_str(Color.BLUE, "struct")} {node.value}\n {indent + left}'
    if node.kind == NodeKind.DECLARATION:
        return f'let {left}: {color_str(Color.GREEN, rev_type_of_ident(node.left.value))} = {right}'
    if node.kind == NodeKind.STRUCT_DECL:
        if node.right is not None:
            return f'let {left}: {color_str(Color.GREEN, rev_type_of(node.ntype))} = {right}'
        else:
            return f'let {node.value}: {color_str(Color.GREEN, rev_type_of(node.ntype))}'
    if node.kind == NodeKind.STRUCT_ELEM_DECL:
        return f'{left}: {color_str(Color.GREEN, rev_type_of_ident(node.left.value))}'
    if node.kind == NodeKind.ARR_DECL:
        arr = Def.arr_map.get(node.value)
        return f'let {node.value}: {color_str(Color.GREEN, rev_type_of(arr.elem_type))}[{arr.elem_cnt}]'
    if node.kind == NodeKind.STRUCT_ARR_DECL:
        arr = Def.arr_map.get(node.value)
        return f'{node.value}: {color_str(Color.GREEN, rev_type_of(arr.elem_type))}[{arr.elem_cnt}]'
    if node.kind == NodeKind.OP_GT:
        return f'({left} > {right})'
    if node.kind == NodeKind.OP_LT:
        return f'({left} < {right})'
    if node.kind == NodeKind.OP_EQ:
        return f'({left} == {right})'
    if node.kind == NodeKind.OP_GTE:
        return f'({left} >= {right})'
    if node.kind == NodeKind.OP_LTE:
        return f'({left} <= {right})'
    if node.kind == NodeKind.OP_NEQ:
        return f'({left} != {right})'
    if node.kind == NodeKind.ARR_ACC:
        return f'{left}[{right}]'
    if node.kind == NodeKind.ELEM_ACC:
        return f'{left}.{right}'
    if node.kind == NodeKind.TERN:
        return f'({left} {color_str(Color.BLUE, "if")} {middle} {color_str(Color.BLUE, "else")} {right})'
    if node.kind == NodeKind.IF:
        body_indent = indent if node.left.kind != NodeKind.GLUE else ''
        return f'{color_str(Color.BLUE, "if")} {middle}\n{body_indent + left}'
    if node.kind == NodeKind.ELIF:
        body_indent = indent if node.left.kind != NodeKind.GLUE else ''
        return f'{color_str(Color.BLUE, "elif")} {middle}\n{body_indent + left}'
    if node.kind == NodeKind.ELSE:
        body_indent = indent if node.left.kind != NodeKind.GLUE else ''
        return f'{color_str(Color.BLUE, "else")}\n{body_indent + left}'
    if node.kind == NodeKind.WHILE:
        body_indent = indent if node.left.kind != NodeKind.GLUE else ''
        return f'{color_str(Color.BLUE, "while")} {left}\n{body_indent + right}'
    if node.kind == NodeKind.FOR:
        body_indent = indent if node.left.kind != NodeKind.GLUE else ''
        return f'{color_str(Color.BLUE, "for")} {middle} in {right})\n{body_indent + left}'
    if node.kind == NodeKind.GLUE:
        left_indent = indent
        if parent and parent.kind == NodeKind.GLUE:
            left_indent = ''
        elif has_indent(node.left.kind):
            left_indent = prev_indent

        if not right:
            return left_indent + left
        else:
            return f'{left_indent + left}\n{indent + right}'
    if node.kind == NodeKind.MOVE:
        return f'move({left})'
    if node.kind == NodeKind.FUN_CALL:
        fun = Def.fun_map.get(node.value)
        sig: Def.FunctionSignature = find_signature(fun, node.left)
        if sig is None:
            def get_type(node: Node):
                return node.ntype

            print_error('ml_walker_step',
                        f'No signature of {fun.name} matches {list(map(Def.rev_type_of, map(get_type, args_to_list(node.left))))} out of {[list(map(Def.rev_type_of, sig.arg_types)) for sig in fun.signatures]}')

        # ? For easy debugging of signatures
        # def get_type(node: Node):
        #     return node.ntype
        # print('DBG:',
        #       f'Call to {fun.name}: {list(map(Def.rev_type_of, map(get_type, args_to_list(node.left))))} fetches {[list(map(Def.rev_type_of, sig.arg_types))]} out of {[list(map(Def.rev_type_of, sig.arg_types)) for sig in fun.signatures]}')

        fun_name = color_str(Color.BLUE, sig.name) if is_special_fun(
            fun.name) else sig.name
        return f'{fun_name}({fun_call_tree_str(node, ml_walk)})'
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

        args_str = ''
        if sig.arg_cnt > 0:
            args_zip = zip(sig.arg_names, sig.arg_types)
            args_map = map(
                lambda t: f'{t[0]}: {color_str(Color.GREEN, rev_type_of(t[1]))}', args_zip)
            args_str = ", ".join(
                list(args_map) + (['...'] if fun.is_variadic else []))

        body_indent = indent if node.left.kind != NodeKind.GLUE else ''
        fun_name = color_str(Color.BLUE, sig_name) if is_special_fun(
            fun_name) else sig_name

        if args_str == '':
            return f'{color_str(Color.BLUE, "fun")} {fun_name}: {color_str(Color.GREEN, rev_type_of(sig.ret_type))}\n{body_indent + left}'
        else:
            return f'{color_str(Color.BLUE, "fun")} {fun_name}({args_str}): {color_str(Color.GREEN, rev_type_of(sig.ret_type))}\n{body_indent + left}'

    if node.kind in (NodeKind.OP_WIDEN, NodeKind.CAST):
        return f'({color_str(Color.GREEN, rev_type_of(node.ntype))}){left}'
    if node.kind == NodeKind.STRFY:
        if node.left.kind == NodeKind.STRFY:
            return ml_walk(node.left)
        else:
            return color_str(Color.WARNING, f"\"{ml_walk(node.left)}\"")
    if node.kind in (NodeKind.SIZE, NodeKind.LIT):
        return f'{color_str(Color.BLUE, node.value)}({left})'
    if node.kind in (NodeKind.TYPE, NodeKind.OFF, NodeKind.LEN, NodeKind.LIT, NodeKind.SIZE, NodeKind.COUNT):
        return ml_walk(ml_expand_builtin(node))
    if node.kind == NodeKind.RET:
        return f'{color_str(Color.BLUE, "ret")} {left if left is not None else ""}'
    if node.kind == NodeKind.BLOCK:
        return f'block {node.value}'
    if node.kind == NodeKind.NAMESPACE:
        return f'namespace {node.value}'
    if node.kind == NodeKind.REF:
        return f'(&({left}))'
    if node.kind == NodeKind.DEREF:
        return f'(*{left})'
    if node.kind == NodeKind.END:
        return indent + color_str(Color.BLUE, 'end')

    print_error('ml_walker_step', f'Invalid node kind {node.kind}')


def ml_walk(node):
    walker = Walker(ml_walker_step)
    return walker.walk(node)
