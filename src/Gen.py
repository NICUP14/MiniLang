import Def
from typing import Optional
from Def import Node
from Def import NodeKind
from Def import Operand
from Def import VariableMetaKind
from Def import VariableType
from Def import Register
from Def import CALL_REGS
from Def import default_ckind
from Def import default_type
from Def import arr_ckind
from Def import ptr_ckind
from Def import ref_ckind
from Def import alloc_reg
from Def import free_reg
from Def import free_all_regs
from Def import modf_of
from Def import node_is_cmp
from Def import cmp_modf_of
from Def import global_modf_of
from Def import size_of
from Def import off_of
from Def import print_error
from Def import print_stdout
from Def import needs_widen
from Def import type_compatible
from Def import rev_type_of
from Def import is_local_ident
from Snippet import Snippet
from Snippet import SnippetCollection
from Snippet import copy_of
import GenStr


# Global label counter
label_idx = 0


def label() -> int:
    global label_idx
    curr_label = label_idx
    label_idx += 1

    return curr_label


def gen_label(label: str) -> None:
    print_stdout(str_snippet(SnippetCollection.LABEL, label).asm())


def gen_reg_swap(opd1: Operand, opd2: Operand):
    if opd1.reg == Register.id_max or opd2.reg == Register.id_max:
        print_error('gen_reg_swap',
                    'Cannot swap unallocated operands')

    kind = opd1.var_type.kind()
    tmp = Operand('', opd1.var_type)
    tmp.reg = alloc_reg(opd=tmp)

    snippet = copy_of(SnippetCollection.MOVE_REG)
    snippet.add_arg(modf_of(opd1.var_type.kind()))
    snippet.add_arg(opd1.reg_str())
    snippet.add_arg(tmp.reg_str())
    print_stdout(snippet.asm())

    snippet = copy_of(SnippetCollection.MOVE_REG)
    snippet.add_arg(modf_of(kind))
    snippet.add_arg(opd2.reg_str())
    snippet.add_arg(opd1.reg_str())
    print_stdout(snippet.asm())

    snippet = copy_of(SnippetCollection.MOVE_REG)
    snippet.add_arg(modf_of(kind))
    snippet.add_arg(tmp.reg_str())
    snippet.add_arg(opd2.reg_str())
    print_stdout(snippet.asm())

    free_reg(tmp.reg)
    opd1.reg, opd2.reg = opd2.reg, opd1.reg


def gen_reg_chown(old_reg: Register, left_opd: Operand, right_opd: Operand) -> Operand:
    if old_reg == left_opd.reg:
        return left_opd
    if old_reg == right_opd.reg:
        return right_opd

    if not Def.reg_avail_map[old_reg]:
        old_opd = Def.opd_map.get(old_reg)
        new_opd = copy_of(old_opd)
        new_opd.reg = alloc_reg(opd=new_opd)
        old_opd.unload()
        new_opd.unload()

        if old_opd is None:
            print_error('gen_reg_chown',
                        f'Cannot get ownership of {old_reg}')

        new_opd.load()
        snippet = bin_snippet(SnippetCollection.MOVE_REG, new_opd, old_opd)
        print_stdout(snippet.asm())

        old_opd.reg = new_opd.reg
        new_opd.reg = old_reg
    else:
        new_opd = copy_of(left_opd)
        new_opd.reg = alloc_reg(old_reg, opd=new_opd)

    return new_opd


def gen_load_imm(opd: Operand) -> None:
    snippet = copy_of(SnippetCollection.LOAD_IMM)
    snippet.add_arg(modf_of(opd.var_type.kind()))
    snippet.add_arg(opd.value)
    snippet.add_arg(opd.reg_str())
    print_stdout(snippet.asm())


def gen_load_str_lit(opd: Operand) -> None:
    snippet = copy_of(SnippetCollection.LOAD_DATA_ADDR)
    snippet.add_arg(modf_of(opd.var_type.kind()))
    snippet.add_arg(opd.value)
    snippet.add_arg(opd.reg_str())
    print_stdout(snippet.asm())


def gen_load_local_str(opd: Operand) -> None:
    name = opd.value
    off = off_of(name)

    snippet = copy_of(SnippetCollection.LOAD_STACK_ADDR)
    snippet.add_arg(modf_of(opd.var_type.kind()))
    snippet.add_arg(f'-{off}')
    snippet.add_arg(opd.reg_str())
    print_stdout(snippet.asm())

    gen_load_ptr(opd)


def gen_load_var(opd: Operand):
    name = opd.value
    off = off_of(name)

    var = Def.var_map[name]

    if var.is_local:
        snippet = copy_of(SnippetCollection.LOAD_STACK_VAR)
        snippet.add_arg(modf_of(opd.var_type.kind()))
        snippet.add_arg(f'-{off}')
        snippet.add_arg(opd.reg_str())
        print_stdout(snippet.asm())
    else:
        snippet = copy_of(SnippetCollection.LOAD_DATA_VAR)
        snippet.add_arg(modf_of(opd.var_type.kind()))
        snippet.add_arg(name)
        snippet.add_arg(opd.reg_str())
        print_stdout(snippet.asm())


def gen_load_ptr(opd: Operand, vtype: VariableType = default_type):
    # if opd.value not in Def.ptr_map:
    #     print_error('gen_load_ptr', f'No such pointer {opd.value}')

    # ? Placeholder
    tmp = copy_of(opd)
    tmp.var_type = vtype

    deref_snippet = bin_snippet(SnippetCollection.DEREF_REG, tmp, opd)
    print_stdout(deref_snippet.asm())


def gen_load_addr(opd: Operand):
    name = opd.value
    off = off_of(name)
    is_local = is_local_ident(name)

    if is_local:
        snippet = copy_of(SnippetCollection.LOAD_STACK_ADDR)
        snippet.add_arg(modf_of(opd.var_type.kind()))
        snippet.add_arg(f'-{off}')
        snippet.add_arg(opd.reg_str())
        print_stdout(snippet.asm())
    else:
        snippet = copy_of(SnippetCollection.LOAD_DATA_ADDR)
        snippet.add_arg(modf_of(opd.var_type.kind()))
        snippet.add_arg(name)
        snippet.add_arg(opd.reg_str())
        print_stdout(snippet.asm())


def gen_load(opd: Operand):
    if opd.is_loaded():
        return

    opd.load()
    if opd.reg == Register.id_max:
        opd.reg = alloc_reg(opd=opd)

    vtype = opd.var_type
    if opd.is_imm():
        if vtype.ckind == ptr_ckind:
            gen_load_str_lit(opd)
        else:
            gen_load_imm(opd)

    else:
        if vtype.meta_kind() in (VariableMetaKind.PRIM, VariableMetaKind.BOOL):
            gen_load_var(opd)
        elif vtype.ckind == arr_ckind:
            gen_load_addr(opd)
        elif vtype.ckind == ptr_ckind:
            gen_load_addr(opd)
            if not opd.is_ref():
                gen_load_ptr(opd)
        elif vtype.ckind == ref_ckind:
            ptr = Def.ptr_map.get(opd.value)
            elem_type = ptr.elem_type

            gen_load_addr(opd)
            gen_load_ptr(opd)
            if not opd.is_ref():
                gen_load_ptr(opd, elem_type)
                opd.var_type = elem_type
                gen_widen(opd)
                opd.var_type = default_type
        else:
            print_error('gen_load', f'Invalid operand type {opd.var_type}')


def gen_write(opd: Operand, opd2: Operand):
    vtype = opd.var_type

    if vtype.meta_kind() == VariableMetaKind.PRIM:
        gen_write_var(opd)
    elif vtype in (arr_ckind, ptr_ckind, ref_ckind):
        gen_write_ref(opd, opd2)
    else:
        print_error('gen_write', f'Invalid operand type {opd.var_type}')


def gen_write_var(opd: Operand):
    name = opd.value
    off = off_of(name)

    # ? Fix for function parameters
    kind = opd.var_type.kind()
    var = Def.var_map.get(name)
    is_ptr = Def.ident_map.get(name) in (
        VariableMetaKind.PTR, VariableMetaKind.REF)

    if is_ptr or var.is_local:
        snippet = copy_of(SnippetCollection.WRITE_STACK_VAR)
        snippet.add_arg(modf_of(kind))
        snippet.add_arg(opd.reg_str())
        snippet.add_arg(f'-{off}')
        print_stdout(snippet.asm())
    else:
        snippet = copy_of(SnippetCollection.WRITE_DATA_VAR)
        snippet.add_arg(modf_of(kind))
        snippet.add_arg(opd.reg_str())
        snippet.add_arg(name)
        print_stdout(snippet.asm())


def gen_write_ref(left_opd: Operand, right_opd: Operand, is_acc: bool = False):
    vtype = left_opd.var_type
    if is_acc and vtype.ckind == arr_ckind:
        vtype = Def.arr_map[left_opd.value].elem_type
    if is_acc and vtype.ckind in (ptr_ckind, ref_ckind):
        vtype = Def.ptr_map[left_opd.value].elem_type

    opd: Operand = copy_of(right_opd)
    opd.var_type = vtype

    snippet = copy_of(SnippetCollection.WRITEREF_REG)
    snippet.add_arg(modf_of(vtype.kind()))
    snippet.add_arg(opd.reg_str())
    snippet.add_arg(left_opd.reg_str())
    print_stdout(snippet.asm())


def gen_widen(opd: Operand, var_type: VariableType = default_type):
    if opd.var_type == var_type:
        return

    opd2 = copy_of(opd)
    opd.var_type = var_type
    snippet = copy_of(SnippetCollection.EXTEND_REG)
    snippet.add_arg(opd2.reg_str())
    snippet.add_arg(opd.reg_str())
    print_stdout(snippet.asm())


def gen_if_tree(node: Node):
    false_label = label()
    end_label = label() if node.right else 0

    gen_tree(node.middle, node, false_label)
    free_all_regs()
    gen_tree(node.left, node, -1)
    free_all_regs()

    if node.right is not None:
        snippet = copy_of(SnippetCollection.JMP)
        snippet.add_arg(str(end_label))
        print_stdout(snippet.asm())

    snippet = copy_of(SnippetCollection.LABEL)
    snippet.add_arg(str(false_label))
    print_stdout(snippet.asm())

    if node.right is not None:
        gen_tree(node.right, node, -1)
        free_all_regs()

        snippet = copy_of(SnippetCollection.LABEL)
        snippet.add_arg(str(end_label))
        print_stdout(snippet.asm())


def gen_while_tree(node: Node):
    start_label = label()
    end_label = label()

    snippet = copy_of(SnippetCollection.LABEL)
    snippet.add_arg(str(start_label))
    print_stdout(snippet.asm())

    gen_tree(node.left, node, end_label)
    free_all_regs()
    gen_tree(node.right, node, -1)
    free_all_regs()

    jmp_snippet = copy_of(SnippetCollection.JMP)
    jmp_snippet.add_arg(str(start_label))
    print_stdout(jmp_snippet.asm())

    label_snippet = copy_of(SnippetCollection.LABEL)
    label_snippet.add_arg(str(end_label))
    print_stdout(label_snippet.asm())


# ? Work in progress
def gen_fun_call(node: Node):
    reg_cnt = -1
    glue_node = node.left
    while glue_node is not None:
        reg_cnt += 1
        glue_node = glue_node.left

    arg_cnt = 0
    name = node.value
    fun = Def.fun_map.get(name)

    if fun.arg_cnt > 0:
        glue_node = node.left

        # Fix for single-argument functions
        if glue_node.kind != NodeKind.GLUE:
            arg_cnt = 1

            opd = gen_tree(glue_node, node, -1)
            opd_dst = Operand('', opd.var_type, CALL_REGS[0])

            if not type_compatible(NodeKind.FUN_CALL, opd.var_type.ckind, fun.arg_types[0].ckind):
                print_error('gen_fun_call',
                            f'Incompatible type in {name}\'s function call (name={fun.arg_names[0]}, type1={rev_type_of(opd.var_type)}, type2={rev_type_of(fun.arg_types[0])}, param_idx=0)', node=node)

            # ?Temporary
            gen_load(opd)

            snippet = copy_of(SnippetCollection.MOVE_REG)
            snippet.add_arg(modf_of(opd.var_type.kind()))
            snippet.add_arg(opd.reg_str())
            snippet.add_arg(opd_dst.reg_str())
            print_stdout(snippet.asm())

            free_reg(opd.reg)
            free_reg(opd_dst.reg)

        else:
            arg_cnt = reg_cnt + 1
            # arg_cnt = reg_cnt + 1

            while glue_node is not None:
                opd = gen_tree(glue_node.right, glue_node, -1)
                opd_dst = Operand('', opd.var_type, CALL_REGS[reg_cnt])

                if reg_cnt < fun.arg_cnt and not type_compatible(NodeKind.FUN_CALL, opd.var_type.ckind, fun.arg_types[reg_cnt].ckind):
                    print_error('gen_fun_call',
                                f'Incompatible type in {name}\'s function call (name={fun.arg_names[reg_cnt]}, type1={rev_type_of(opd.var_type)}, type2={rev_type_of(fun.arg_types[reg_cnt])}, param_idx={reg_cnt})', node=node)

                # ?Temporary
                gen_load(opd)

                snippet = copy_of(SnippetCollection.MOVE_REG)
                snippet.add_arg(modf_of(opd.var_type.kind()))
                snippet.add_arg(opd.reg_str())
                snippet.add_arg(opd_dst.reg_str())
                print_stdout(snippet.asm())

                free_reg(opd.reg)
                free_reg(opd_dst.reg)

                glue_node = glue_node.left
                reg_cnt -= 1

    if fun.is_variadic:
        if arg_cnt < fun.arg_cnt:
            print_error('gen_fun_call',
                        f'Variadic function {fun.name} expects {fun.arg_cnt} parameters, but only {arg_cnt} were provided', node=node)
    elif arg_cnt != fun.arg_cnt:
        print_error('gen_fun_call',
                    f'Function {fun.name} expects {fun.arg_cnt} parameters, but only {arg_cnt} were provided', node=node)

    if fun.is_variadic:
        snippet = copy_of(SnippetCollection.XOR_RAX)
        print_stdout(snippet.asm())

    for reg in CALL_REGS:
        alloc_reg(reg)
    snippet = copy_of(SnippetCollection.CALL)
    snippet.add_arg(node.value)
    print_stdout(snippet.asm())

    for reg in CALL_REGS:
        free_reg(reg)

    alloc_reg(Register.rax)
    return Operand('', fun.ret_type, Register.rax, True)


# TODO: Replace the print with a snippet.
def gen_sub_stack(off: int):
    print_stdout(f'sub ${off}, %rsp')


def str_snippet(snippet_base: Snippet, arg: str):
    snippet = copy_of(snippet_base)
    snippet.add_arg(arg)
    return snippet


def bin_snippet(snippet_base: Snippet, left_opd: Operand, right_opd: Operand) -> Snippet:
    '''
    left_opd: src
    right_opd: dest
    '''

    snippet = copy_of(snippet_base)
    snippet.add_arg(modf_of(left_opd.var_type.kind()))
    snippet.add_arg(right_opd.reg_str())
    snippet.add_arg(left_opd.reg_str())
    return snippet


def gen_preamble():
    # ? Unused
    # print_stdout('.set ml_cstdlib_exit, exit')
    # print_stdout('.set ml_cstdlib_printf, printf')
    # print_stdout('.set ml_cstdlib_scanf, scanf')
    # print_stdout('.set ml_cstdlib_puts, puts')
    # print_stdout('.set ml_cstdlib_malloc, malloc')
    # print_stdout('.set ml_cstdlib_free, free')
    # print_stdout('.set ml_cstdlib_memset, memset')
    # print_stdout('.set ml_cstdlib_memcpy, memcpy')
    # print_stdout('.set ml_cstdlib_strlen, strlen')
    # print_stdout('.set ml_cstdlib_strcpy, strcpy')
    # print_stdout('.set ml_cstdlib_strncpy, strncpy')
    # print_stdout('.set ml_cstdlib_strcmp, strcmp')
    # print_stdout('.set ml_cstdlib_strncmp, strncmp')
    # print_stdout('.set ml_cstdlib_strcat, strcat')
    # print_stdout('.set ml_cstdlib_strncat, strncat')
    # print_stdout('.set ml_cstdlib_strchr, strchr')
    # print_stdout('.set ml_cstdlib_strrchr, strrchr')
    # print_stdout('.set ml_cstdlib_strstr, strstr')
    # print_stdout('.set ml_cstdlib_isdigit, isdigit')
    # print_stdout('.set ml_cstdlib_atoi, atoi')
    # print_stdout('.set ml_cstdlib_abs, abs')
    # print_stdout('.set ml_cstdlib_labs, labs')
    # print_stdout('.set ml_cstdlib_rand, rand')
    # print_stdout('.set ml_cstdlib_srand, srand')
    pass


def gen_postamble():

    def is_fun(item):
        _, value = item
        return value == VariableMetaKind.FUN

    print_stdout()
    for fun_name, _ in list(filter(is_fun, Def.ident_map.items())):
        fun = Def.fun_map.get(fun_name)
        if fun.is_extern:
            print_stdout(f'.extern {fun_name}')
        else:
            print_stdout(f'.global {fun_name}')
    print_stdout()

    print_stdout('.data')
    for (string, label) in Def.str_lit_map.items():
        print_stdout(f'{label}: .asciz \"{string}\"')

    for (ident, _) in Def.ident_map.items():
        meta_kind = Def.ident_map.get(ident)
        if meta_kind in (VariableMetaKind.FUN, VariableMetaKind.MACRO) or (
                is_local_ident(ident)):
            continue

        value = 0
        vtype = default_type
        if meta_kind in (VariableMetaKind.PRIM, VariableMetaKind.BOOL):
            var = Def.var_map.get(ident)
            value = var.value
            vtype = var.vtype

        if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF):
            value = Def.ptr_map.get(ident).value

        if meta_kind == VariableMetaKind.ARR:
            value = Def.arr_map.get(ident).value

        print_stdout(
            f'{ident}: {global_modf_of(vtype.kind())} {value}')

    if Def.ident_map.get('main') != VariableMetaKind.FUN:
        print_error('gen_postamble',
                    'The program has no entry point; Reference to main does not exist')


def gen_fun_preamble(name: str):
    snippet = copy_of(SnippetCollection.FUN_PREAMBLE)
    snippet.add_arg(name)
    print_stdout(snippet.asm())

    fun = Def.fun_map.get(name)

    gen_sub_stack(fun.off)

    for arg_idx in range(fun.arg_cnt - 1, -1, -1):
        arg_name = f'{name}_{fun.arg_names[arg_idx]}'
        opd = Operand(arg_name,
                      fun.arg_types[arg_idx], CALL_REGS[arg_idx])
        gen_write_var(opd)


def gen_fun_postamble():
    snippet = copy_of(SnippetCollection.FUN_POSTAMBLE)
    print_stdout(snippet.asm())


def gen(node: Node):
    gen_preamble()
    gen_tree(node, None, -1)
    gen_postamble()


def opposite_of(kind: NodeKind) -> NodeKind:
    kind_map = {
        NodeKind.OP_EQ: NodeKind.OP_NEQ,
        NodeKind.OP_NEQ: NodeKind.OP_EQ,
        NodeKind.OP_GT: NodeKind.OP_LTE,
        NodeKind.OP_LT: NodeKind.OP_GTE,
        NodeKind.OP_GTE: NodeKind.OP_LT,
        NodeKind.OP_LTE: NodeKind.OP_GT
    }

    if kind not in kind_map:
        print_error('opposite_of', f'Invalid node kind {kind}')

    return kind_map.get(kind)


def gen_tree(node: Node, parent: Optional[Node], curr_label: int):
    left_opd = None
    right_opd = None

    if node is None:
        return

    if Def.comments_enabled and node.kind in (NodeKind.OP_ASSIGN,
                                                      NodeKind.DECLARATION,
                                                      NodeKind.IF,
                                                      NodeKind.WHILE,
                                                      NodeKind.RET,
                                                      NodeKind.FUN,
                                                      NodeKind.ASM,
                                                      NodeKind.FUN_CALL):
        # Local function variable
        if node.kind == NodeKind.FUN:
            for name, meta_kind in Def.ident_map.items():
                if name.startswith(node.value) and meta_kind != VariableMetaKind.FUN:
                    snippet = copy_of(SnippetCollection.CMT)
                    snippet.add_arg(f'| {name}: -{off_of(name)}(%rbp)')
                    print_stdout(snippet.asm())

        body = GenStr.tree_str(node)
        for line in body.split('\n'):
            snippet = copy_of(SnippetCollection.CMT)
            snippet.add_arg(f'| {line}')
            print_stdout(snippet.asm())

    # If statement
    if node.kind == NodeKind.IF:
        gen_if_tree(node)
        return None

    # While statement
    if node.kind == NodeKind.WHILE:
        gen_while_tree(node)
        return None

    if node.kind == NodeKind.FUN:
        gen_fun_preamble(node.value)
        gen_tree(node.left, node, -1)
        gen_fun_postamble()
        free_all_regs()
        return None

    if node.kind == NodeKind.RET:
        alloc_reg(Register.rax)
        opd = gen_tree(node.left, node, - 1)
        opd_dst = Operand(node.value, node.ntype, Register.rax)
        gen_load(opd)

        snippet = bin_snippet(SnippetCollection.MOVE_REG, opd_dst, opd)
        print_stdout(snippet.asm())
        gen_fun_postamble()
        free_all_regs()
        return None

    if node.kind == NodeKind.FUN_CALL:
        return gen_fun_call(node)

    if node.kind == NodeKind.TYPE:
        # opd = gen_tree(node.left, node, -1)
        # free_reg(opd.reg)
        return gen_tree(Node(NodeKind.STR_LIT, node.ntype, rev_type_of(node.left.ntype)), node, -1)

    if node.kind == NodeKind.OFF:
        if node.left.kind != NodeKind.IDENT:
            return gen_tree(Node(NodeKind.INT_LIT, node.ntype, '0'), node, -1)
            # print_error('gen_tree',
            #             f'The off_of builtin accepts only identifiers, got {node.left.kind}')

        return gen_tree(Node(NodeKind.INT_LIT, node.ntype, str(off_of(node.left.value))), node, -1)

    if node.kind == NodeKind.LEN:
        if node.left.kind != NodeKind.IDENT:
            return gen_tree(Node(NodeKind.INT_LIT, node.ntype, '0'), node, -1)
            # print_error('gen_tree',
            #             f'The len_of builtin accepts only identifiers, got {node.left.kind}')

        ident = node.left.value
        meta_kind = Def.ident_map.get(ident)
        if ident not in Def.ident_map:
            print_error('to_tree',
                        f'The len_of builtin only accepts pre-declared identifiers, got {ident}')
        # if meta_kind not in (VariableMetaKind.ARR, VariableMetaKind.PTR):
        #     print_error('to_tree',
        #                 f'The len_of builtin only accepts array/pointer identifiers, got {meta_kind}')

        elem_cnt = 0
        if meta_kind == VariableMetaKind.ARR:
            arr = Def.arr_map.get(ident)
            elem_cnt = arr.elem_cnt
        if meta_kind == VariableMetaKind.PTR:
            ptr = Def.ptr_map.get(ident)
            elem_cnt = ptr.elem_cnt

        return gen_tree(Node(NodeKind.INT_LIT, node.ntype, str(elem_cnt)), node, -1)

    if node.kind == NodeKind.SIZE:
        if node.left.kind != NodeKind.IDENT:
            return gen_tree(Node(NodeKind.INT_LIT, node.ntype, '0'), node, -1)
            # print_error('gen_tree',
            #             f'The size_of builtin accepts only identifiers, got {node.left.kind}')

        size = Def.size_of_ident(node.left.value)
        return gen_tree(Node(NodeKind.INT_LIT, node.ntype, str(size)), node, -1)

    if node.kind == NodeKind.CAST:
        opd = gen_tree(node.left, node, -1)
        if opd is None:
            print_error('gen_tree',
                        f'Cannot cast the expression (kind={node.left.kind}, type={rev_type_of(node.left.ntype)})', node=node)

        if needs_widen(opd.var_type.ckind, node.ntype.ckind) == 1:
            gen_load(opd)
            gen_widen(opd, node.ntype)
        return opd

    if node.kind == NodeKind.ASM:
        if node.left.kind != NodeKind.STR_LIT:
            print_error(
                'gen_tree', 'The asm builtin only accepts string literals', node=node)

        print_stdout(node.left.value.lstrip('\"').rstrip('\"'))
        return None

    if node.kind == NodeKind.END:
        return None

    # Glue statement
    if node.kind == NodeKind.GLUE:
        gen_tree(node.left, node, -1)
        free_all_regs()
        gen_tree(node.right, node, -1)
        free_all_regs()
        return None

    if (node.left is not None):
        left_opd = gen_tree(node.left, node, -1)
    if (node.right is not None):
        right_opd = gen_tree(node.right, node, -1)

    if node.kind == NodeKind.OP_WIDEN:
        gen_load(left_opd)
        gen_widen(left_opd, node.ntype)
        return left_opd

    if node.kind == NodeKind.INT_LIT:
        opd = Operand(node.value, node.ntype, imm=True)
        opd.reg = alloc_reg(opd=opd)
        return opd

    if node.kind in (NodeKind.TRUE_LIT, NodeKind.FALSE_LIT):
        opd = Operand(Def.BOOL_VALUES.get(node.value), node.ntype, imm=True)
        opd.reg = alloc_reg(opd=opd)
        return opd

    if node.kind == NodeKind.CHAR_LIT:
        value = node.value.lstrip('\'').rstrip('\'')
        opd = Operand(
            ord(bytes(value, 'utf-8').decode('unicode_escape')), node.ntype, imm=True)
        opd.reg = alloc_reg(opd=opd)
        return opd

    if node.kind == NodeKind.STR_LIT:
        string = node.value.lstrip('\"').rstrip(
            '\"').replace('\n', '\\n').replace('\t', '\\t').replace('\\end', 'end')
        value = ""

        if string not in Def.str_lit_map:
            Def.str_lit_map[string] = f'str_{len(Def.str_lit_map)}'
        value = Def.str_lit_map.get(string)

        opd = Operand(value, node.ntype, imm=True)
        opd.reg = alloc_reg(opd=opd)
        return opd

    if node.kind == NodeKind.IDENT:
        opd = Operand(node.value, node.ntype, Register.id_max)
        return opd

    # Reference
    if node.kind == NodeKind.REF:
        opd: Operand = copy_of(left_opd)
        opd.ref = left_opd.var_type.ckind != ref_ckind
        opd.var_type = VariableType(
            ptr_ckind, left_opd.var_type.ckind)
        opd.value = node.left.value
        return opd

    # Dereference
    if node.kind == NodeKind.DEREF:
        if node != parent.left or parent.kind not in (NodeKind.OP_ASSIGN, NodeKind.DECLARATION):
            if left_opd.var_type.ckind == ptr_ckind:
                ptr = Def.ptr_map.get(left_opd.value)
                elem_type = ptr.elem_type

            if left_opd.var_type.ckind == arr_ckind:
                arr = Def.arr_map.get(left_opd.value)
                elem_type = arr.elem_type

            gen_load(left_opd)
            gen_load_ptr(left_opd, elem_type)
            left_opd.var_type = elem_type
            gen_widen(left_opd)
            left_opd.var_type = default_type

        return left_opd

    # Array access
    if node.kind == NodeKind.ARR_ACC:
        gen_load(left_opd)
        gen_load(right_opd)
        opd = Operand(str(size_of(left_opd.var_type.elem_ckind)),
                      VariableType(right_opd.var_type.elem_ckind), imm=True)
        opd.reg = alloc_reg(opd=opd)
        gen_load(opd)

        mul_snippet = bin_snippet(SnippetCollection.MUL_OP, opd, right_opd)
        # sub_snippet = bin_snippet(
        #     SnippetCollection.SUB_OP, left_opd, opd)
        add_snippet = bin_snippet(
            SnippetCollection.ADD_OP, left_opd, opd)
        print_stdout(mul_snippet.asm())
        print_stdout(add_snippet.asm())
        # print_stdout(sub_snippet.asm())

        if node != parent.left or parent.kind not in (NodeKind.OP_ASSIGN, NodeKind.DECLARATION):
            # ?Duplicated code block
            if left_opd.var_type.ckind == arr_ckind:
                arr = Def.arr_map.get(left_opd.value)
                elem_type = arr.elem_type
                gen_load_ptr(left_opd, elem_type)

                left_opd.var_type = elem_type
                left_opd.load()
                if needs_widen(left_opd.var_type.ckind, default_ckind) == 1:
                    gen_widen(left_opd)

            elif left_opd.var_type.ckind == ptr_ckind:
                ptr = Def.ptr_map.get(left_opd.value)
                elem_type = ptr.elem_type
                gen_load_ptr(left_opd, elem_type)

                left_opd.var_type = elem_type
                left_opd.load()
                if needs_widen(left_opd.var_type.ckind, default_ckind) == 1:
                    gen_widen(left_opd)

            else:
                gen_load_ptr(left_opd)

        free_reg(right_opd.reg)
        free_reg(opd.reg)
        return left_opd

    # Assignment & Declaration
    if node.kind in (NodeKind.OP_ASSIGN, NodeKind.DECLARATION):
        gen_load(right_opd)
        if needs_widen(left_opd.var_type.ckind, right_opd.var_type.ckind) == 2:
            gen_widen(right_opd)
            right_opd.var_type = default_type

        opd = copy_of(left_opd)
        vtype = opd.var_type.ckind
        if vtype in (arr_ckind, ptr_ckind, ref_ckind):
            if opd.reg == Register.id_max:
                opd.reg = alloc_reg(opd=opd)

            if node.left.kind == NodeKind.IDENT:
                gen_load_addr(opd)

                if vtype == ref_ckind and node.kind != NodeKind.DECLARATION:
                    gen_load_ptr(opd)

            if node.left.kind == NodeKind.DEREF:
                gen_load_addr(opd)
                gen_load_ptr(opd)

            # is_deref =  opd.var_type.ckind == ref_ckind or (
            #    node.left.kind in (NodeKind.DEREF, NodeKind.ARR_ACC))
            is_deref = (
                node.left.kind in (NodeKind.DEREF, NodeKind.ARR_ACC))
            gen_write_ref(opd, right_opd, is_acc=is_deref)
        else:
            opd.reg = right_opd.reg
            gen_write_var(opd)

        return opd

    # Loading (phase 2)
    gen_load(left_opd)
    gen_load(right_opd)

    # Addition
    if node.kind == NodeKind.OP_ADD:
        snippet = bin_snippet(SnippetCollection.ADD_OP, left_opd, right_opd)
        free_reg(right_opd.reg)
        print_stdout(snippet.asm())
        return left_opd

    # Subtraction
    if node.kind == NodeKind.OP_SUB:
        snippet = bin_snippet(SnippetCollection.SUB_OP, left_opd, right_opd)
        free_reg(right_opd.reg)
        print_stdout(snippet.asm())
        return left_opd

    # Bitwise and
    if node.kind == NodeKind.OP_AND:
        snippet = bin_snippet(
            SnippetCollection.AND_BIT_OP, left_opd, right_opd)
        free_reg(right_opd.reg)
        print_stdout(snippet.asm())
        return left_opd

    # Bitwise or
    if node.kind == NodeKind.OP_OR:
        snippet = bin_snippet(
            SnippetCollection.OR_BIT_OP, left_opd, right_opd)
        free_reg(right_opd.reg)
        print_stdout(snippet.asm())
        return left_opd

    # Multiplication
    if node.kind == NodeKind.OP_MULT:
        xor_snippet = copy_of(SnippetCollection.XOR_RDX)
        snippet = bin_snippet(SnippetCollection.MUL_OP, left_opd, right_opd)
        print_stdout(xor_snippet.asm())
        print_stdout(snippet.asm())
        free_reg(right_opd.reg)
        return left_opd

    # Division/Modulo
    if node.kind in (NodeKind.OP_DIV, NodeKind.OP_MOD):
        in_reg = Register.rax
        out_reg = Register.rax if node.kind == NodeKind.OP_DIV else Register.rdx

        div_opd = right_opd
        in_opd = left_opd
        out_opd = gen_reg_chown(out_reg, left_opd, right_opd)

        # print(f'DBG: {left_opd.value} {right_opd.value}')
        # print(f'DBG: {in_opd.value} {out_opd.value}')
        # print(f'DBG: {in_opd.value} / {div_opd.value} = {out_opd.value}')

        if div_opd.reg == Register.rdx:
            new_opd = copy_of(div_opd)
            new_opd.reg = alloc_reg(opd=new_opd)
            gen_reg_swap(div_opd, new_opd)
            free_reg(new_opd.reg)

        if in_opd.reg != in_reg:
            opd = Def.opd_map.get(Register.rax)
            gen_reg_swap(in_opd, opd)

        # if in_opd.reg != in_reg:
        #     gen_reg_swap(in_opd, right_opd)

        snippet = copy_of(SnippetCollection.XOR_RDX)
        print_stdout(snippet.asm())

        snippet = copy_of(SnippetCollection.DIV_MOD_OP)
        snippet.add_arg(div_opd.reg_str())
        print_stdout(snippet.asm())

        free_reg(div_opd.reg)
        if in_opd.reg != out_opd.reg:
            free_reg(in_opd.reg)

        return out_opd

    # Division/Modulo
    # if node.kind in (NodeKind.OP_DIV, NodeKind.OP_MOD):
    #    in_reg = Register.rax
    #    out_reg = Register.rax if node.kind == NodeKind.OP_DIV else Register.rdx
    #    new_opd = gen_reg_chown(out_reg, left_opd, right_opd)
    #    old_opd = left_opd

    #    # left_opd.reg => rax (in)
    #    # right_opd.reg => reg (div)
    #    #! Duplicated code block
    #    if right_opd.reg == in_reg:
    #        kind = left_opd.var_type.kind()
    #        tmp = Operand('', left_opd.var_type)
    #        tmp.reg = alloc_reg(opd=tmp)

    #        snippet = copy_of(SnippetCollection.MOVE_REG)
    #        snippet.add_arg(modf_of(left_opd.var_type.kind()))
    #        snippet.add_arg(left_opd.reg_str())
    #        snippet.add_arg(tmp.reg_str())
    #        print_stdout(snippet.asm())

    #        snippet = copy_of(SnippetCollection.MOVE_REG)
    #        snippet.add_arg(modf_of(kind))
    #        snippet.add_arg(right_opd.reg_str())
    #        snippet.add_arg(left_opd.reg_str())
    #        print_stdout(snippet.asm())

    #        snippet = copy_of(SnippetCollection.MOVE_REG)
    #        snippet.add_arg(modf_of(kind))
    #        snippet.add_arg(tmp.reg_str())
    #        snippet.add_arg(right_opd.reg_str())
    #        print_stdout(snippet.asm())

    #        free_reg(tmp.reg)

    #    if node.kind == NodeKind.OP_MOD and right_opd.reg == out_reg:
    #        kind = left_opd.var_type.kind()
    #        tmp = Operand('', left_opd.var_type)
    #        tmp.reg = alloc_reg(opd=tmp)

    #        snippet = copy_of(SnippetCollection.MOVE_REG)
    #        snippet.add_arg(modf_of(left_opd.var_type.kind()))
    #        snippet.add_arg(left_opd.reg_str())
    #        snippet.add_arg(tmp.reg_str())
    #        print_stdout(snippet.asm())

    #        snippet = copy_of(SnippetCollection.MOVE_REG)
    #        snippet.add_arg(modf_of(kind))
    #        snippet.add_arg(right_opd.reg_str())
    #        snippet.add_arg(left_opd.reg_str())
    #        print_stdout(snippet.asm())

    #        snippet = copy_of(SnippetCollection.MOVE_REG)
    #        snippet.add_arg(modf_of(kind))
    #        snippet.add_arg(tmp.reg_str())
    #        snippet.add_arg(right_opd.reg_str())
    #        print_stdout(snippet.asm())

    #        free_reg(tmp.reg)

    #    snippet = copy_of(SnippetCollection.XOR_RDX)
    #    print_stdout(snippet.asm())

    #    snippet = copy_of(SnippetCollection.DIV_MOD_OP)
    #    snippet.add_arg(old_opd.reg_str())
    #    print_stdout(snippet.asm())
    #    free_reg(old_opd.reg)

    #    return new_opd

    # Comparison
    if node_is_cmp(node.kind):
        cmp_snippet = copy_of(SnippetCollection.CMP_REG)
        cmp_snippet.add_arg(right_opd.reg_str())
        cmp_snippet.add_arg(left_opd.reg_str())
        print_stdout(cmp_snippet.asm())
        opd = copy_of(left_opd)
        opd.var_type = node.ntype

        if parent.kind not in (NodeKind.IF, NodeKind.WHILE):
            set_snippet = copy_of(SnippetCollection.SET_REG)
            set_snippet.add_arg(cmp_modf_of(node.kind))
            set_snippet.add_arg(opd.reg_str())
            print_stdout(set_snippet.asm())
        else:
            jmp_snippet = copy_of(SnippetCollection.COND_JMP)
            jmp_snippet.add_arg(cmp_modf_of(opposite_of(node.kind)))
            jmp_snippet.add_arg(str(curr_label))
            print_stdout(jmp_snippet.asm())

        free_reg(right_opd.reg)
        return opd

    print_error('gen_tree', f'Invalid node kind: {node.kind}')
