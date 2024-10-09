import Def
from Def import Node
from Def import NodeKind
from Def import Color
from Def import color_str
from Def import print_error
from Def import find_signature
from Def import args_to_list

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
    # prev_indent = '  ' * (indent_cnt - 1)
    add_left_semi = node.left is not None and has_semicolon(node.left.kind)
    add_right_semi = node.right is not None and has_semicolon(node.right.kind)

    if node.kind in (NodeKind.INT_LIT, NodeKind.FLOAT_LIT, NodeKind.CHAR_LIT):
        return node.value
    if node.kind in (NodeKind.TRUE_LIT, NodeKind.FALSE_LIT):
        return color_str(Color.BLUE, node.value)
    if node.kind == NodeKind.FUN_LIT:
        return node.ntype.name
    if node.kind == NodeKind.STR_LIT:
        string = node.value.replace('\n', '\\n').replace(
            '\t', '\\t').replace('\\end', 'end')
        return string
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
    if node.kind == NodeKind.OP_NOT:
        return f'(!{left})'
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
    if node.kind in (NodeKind.SIG_DECL, NodeKind.STRUCT_SIG_DECL):
        sig = Def.sig_map.get(node.ntype.name)
        args_str = ', '.join(map(c_rev_type_of, sig.arg_types))

        if node.kind == NodeKind.STRUCT_SIG_DECL:
            return f'{color_str(Color.GREEN, c_rev_type_of(sig.ret_type))} (*{left})({args_str})'
        else:
            return f'{color_str(Color.GREEN, c_rev_type_of(sig.ret_type))} (*{left})({args_str}) = {sig.name}'

    if node.kind == NodeKind.STRUCT_ARR_DECL:
        arr = Def.arr_map.get(node.value)
        return f'{color_str(Color.GREEN, c_rev_type_of(arr.elem_type))} {node.value}[{arr.elem_cnt}]'
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
        # print('DBG:', node.left.value, Def.rev_type_of(node.left.ntype))
        if Def.ident_map.get(node.left.value) == Def.VariableMetaKind.REF or node.left.ntype.ckind == Def.ref_ckind:
            return f'{left}->{right}'
        else:
            return f'{left}.{right}'
    if node.kind == NodeKind.TERN:
        return f'({middle} ? {left} : {right})'
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
    if node.kind == NodeKind.FOR:
        return f'{color_str(Color.BLUE, "for")} (;{middle};{right}) {"{"}\n{left}{";" if add_right_semi else ""}'
    if node.kind == NodeKind.GLUE:
        empty_str = ''
        add_indent = parent is not None and parent.kind != NodeKind.GLUE
        if left is None:
            return f'{indent if add_indent else empty_str}{right}{";" if add_right_semi else empty_str}'
        if right is None:
            return f'{indent if add_indent else empty_str}{left}{";" if add_left_semi else empty_str}'
        else:
            return f'{indent if add_indent else empty_str}{left}{";" if add_left_semi else empty_str}\n{indent + right}{";" if add_right_semi else empty_str}'
    if node.kind == NodeKind.MOVE:
        return left
    if node.kind in (NodeKind.FUN_CALL, NodeKind.SIG_CALL):
        def get_type(node: Node):
            return node.ntype

        def type_compatible(tpl):
            kind, ckind, ckind2 = tpl
            return Def.type_compatible(kind, ckind, ckind2)

        def sig_compat(tpl):
            var_type1, var_type2 = tpl
            return type_compatible((NodeKind.FUN_CALL, var_type1.ckind, var_type2.ckind))

        fun = Def.fun_map.get(node.value)
        sig = None
        if node.kind == NodeKind.SIG_CALL:
            sig = Def.sig_map.get(node.value)
        else:
            sig: Def.FunctionSignature = find_signature(
                fun, node.left, use_gen=False)

        if sig is None or (node.kind == NodeKind.SIG_CALL and not all(map(sig_compat, zip(map(get_type, args_to_list(node.left)), sig.arg_types)))):
            fun_str = ''
            prelude = ''
            if node.kind == NodeKind.FUN_CALL:
                fun_str = fun.name
                prelude = f'No signature of {fun_str} matches'
            if node.kind == NodeKind.SIG_CALL:
                fun_str = node.value
                prelude = f'No arguments of signature {fun_str} matches'

            def _rev_type_of(var_type) -> str:
                if var_type.ckind != Def.sig_ckind:
                    return Def.rev_type_of(var_type)
                if var_type.name in Def.fun_map:
                    return f'sig{[Def.rev_type_of(arg_type) for arg_type in Def.fun_map.get(var_type.name).arg_types]}'
                if var_type.name in Def.sig_map:
                    return f'sig{[Def.rev_type_of(arg_type) for arg_type in Def.sig_map.get(var_type.name).arg_types]}'

            mismatch_msg = f'\n{prelude} {list(map(_rev_type_of, map(get_type, args_to_list(node.left))))} out of {list(map(Def.rev_type_of, sig.arg_types)) if node.kind == NodeKind.SIG_CALL else [list(map(_rev_type_of, sig.arg_types)) for sig in fun.signatures]}.'

            # Prints a help message for functions with empty signature lists. It means that the function is defined by a macro
            missing_msg = f'\nMissing function definition of {fun.name}; It\'s defined within the body of a macro.'

            print_error('c_walker_step',
                        ' '.join([f'{fun_str}({fun_call_tree_str(node, _c_walk)})', missing_msg if len(fun.signatures) == 0 else mismatch_msg]))

        # ? For easy debugging of signatures
        # def get_type(node: Node):
        #     return node.ntype
        # print('DBG:',
        #       f'Call to {fun.name}: {list(map(Def.rev_type_of, map(get_type, args_to_list(node.left))))} fetches {[list(map(Def.rev_type_of, sig.arg_types))]} out of {[list(map(Def.rev_type_of, sig.arg_types)) for sig in fun.signatures]}')

        fun_str = sig.name if node.kind == NodeKind.FUN_CALL else f'(*{node.value})'
        call_str = f'{fun_str}({fun_call_tree_str(node, _c_walk)})'
        if sig.ret_type.meta_kind() in (Def.VariableMetaKind.REF, Def.VariableMetaKind.RV_REF) and (
                parent is None or parent.kind not in (NodeKind.REF, NodeKind.DECLARATION)):
            return f'*{call_str}'
        else:
            return call_str

    if node.kind == NodeKind.ASM:
        return f'{color_str(Color.BLUE, node.value)}({node.left.value})'
    if node.kind == NodeKind.FUN:
        def arg_rev_type_of(tpl):
            name, var_type = tpl
            if var_type.ckind == Def.sig_ckind:
                return f'{color_str(Color.BLUE, c_rev_type_of(var_type))}'
            else:
                return f'{color_str(Color.BLUE, c_rev_type_of(var_type))} {name}'

        sig_name = node.value
        fun_name = Def.fun_sig_map.get(node.value)
        fun = Def.fun_map.get(fun_name)

        # ? Temporary
        sig = None
        for signature in fun.signatures:
            if signature.name == sig_name:
                sig = signature

        args_str = 'void'
        if sig.arg_cnt > 0:
            args_zip = zip(sig.arg_names, sig.arg_types)
            args_map = map(
                arg_rev_type_of, args_zip)
            args_str = ", ".join(
                list(args_map) + (['...'] if fun.is_variadic else []))

        return f'{color_str(Color.GREEN, c_rev_type_of(sig.ret_type))} {node.value}({args_str}) {"{"} \n{left}{";" if add_left_semi else ""}'

    if node.kind in (NodeKind.OP_WIDEN, NodeKind.CAST):
        return f'({color_str(Color.GREEN, c_rev_type_of(node.ntype))}){left}'
    if node.kind == NodeKind.GROUP:
        return left
    if node.kind == NodeKind.STRFY:
        if node.left.kind == NodeKind.STRFY:
            return _c_walk(node.left)
        else:
            return f"\"{_c_walk(node.left)}\""
    if node.kind in (NodeKind.TYPE, NodeKind.OFF, NodeKind.LEN, NodeKind.LIT, NodeKind.SIZE, NodeKind.COUNT):
        return _c_walk(c_expand_builtin(node))
    if node.kind == NodeKind.RET:
        return f'{color_str(Color.BLUE, "return")} {left if left is not None else ""}'
    if node.kind in (NodeKind.NAMESPACE, NodeKind.BLOCK):
        return left
    if node.kind == NodeKind.REF:
        if Def.ident_map.get(node.left.value) in (Def.VariableMetaKind.REF, Def.VariableMetaKind.ARR):
            return left
        else:
            return f'(&({left}))'
    if node.kind == NodeKind.DEREF:
        return f'(*{left})'
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
    funs = """
    inline void* ptr_sub(char* cs, char* cs2) { return (void*)(cs - cs2); }
    inline size_t ptr_dist(char* cs, char* cs2) { return (size_t)(cs - cs2); }
    """

    def trim_tab(s): return s.lstrip(' \t')
    funs_str = '\n'.join(map(trim_tab, funs.split('\n')))

    headers = [
        'stdio.h',
        'stdlib.h',
        'string.h',
        'stdbool.h',
        'ctype.h'
    ]

    def include(header: str) -> str:
        return f'#include <{header}>'

    return '\n'.join(map(include, headers)) + funs_str


def _c_walk(node):
    walker = Walker(c_walker_step)
    return walker.walk(node)


def c_walk(node):
    node = Def.glue_statements([node])
    return f'{_c_preamble()}\n{_c_walk(node)}'
