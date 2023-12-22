import Def
from typing import Optional
from Def import Node
from Def import NodeKind
from Def import Operand
from Def import VariableKind
from Def import VariableMetaKind
from Def import VariableType
from Def import Register
from Def import comments_enabled
from Def import CALL_REGS
from Def import default_type
from Def import arr_type
from Def import ptr_type
from Def import fun_type
from Def import alloc_reg
from Def import free_reg
from Def import free_all_regs
from Def import modf_of
from Def import cmp_modf_of
from Def import global_modf_of
from Def import size_of
from Def import off_of
from Def import print_error
from Def import print_stdout
from Snippet import Snippet
from Snippet import SnippetCollection
from Snippet import copy_of
import GenStr


label_idx = 0


def label() -> int:
    global label_idx
    curr_label = label_idx
    label_idx += 1

    return curr_label


def gen_label(label: int) -> None:
    snippet = copy_of(SnippetCollection.LABEL)
    snippet.add_arg(str(label))
    print_stdout(snippet.asm())


def gen_reg_chown(old_reg: Register, left_opd: Operand, right_opd: Operand) -> Operand:
    if old_reg == left_opd.reg:
        return left_opd
    if old_reg == right_opd.reg:
        return right_opd

    if Def.reg_avail_map[old_reg] == False:
        old_opd = Def.opd_map.get(old_reg)
        new_opd = copy_of(old_opd)
        new_opd.reg = alloc_reg(opd=new_opd)
        old_opd.unload()
        new_opd.unload()

        if old_opd is None:
            print_error('gen_reg_chown',
                        f'Cannot get ownership of {old_reg}')

        new_opd.load()
        snippet = copy_of(SnippetCollection.MOVE_REG)
        snippet.add_arg(modf_of(old_opd.var_type.kind))
        snippet.add_arg(new_opd.reg_str())
        snippet.add_arg(old_opd.reg_str())
        print_stdout(snippet.asm())

        old_opd.reg = new_opd.reg
        new_opd.reg = old_reg
    else:
        new_opd = copy_of(left_opd)
        new_opd.reg = alloc_reg(old_reg, opd=new_opd)

    return new_opd


def gen_load_imm(opd: Operand) -> None:
    snippet = copy_of(SnippetCollection.LOAD_IMM)
    snippet.add_arg(modf_of(opd.var_type.kind))
    snippet.add_arg(opd.value)
    snippet.add_arg(opd.reg_str())
    print_stdout(snippet.asm())


def gen_load_str_lit(opd: Operand) -> None:
    snippet = copy_of(SnippetCollection.LOAD_DATA_ADDR)
    snippet.add_arg(modf_of(opd.var_type.kind))
    snippet.add_arg(opd.value)
    snippet.add_arg(opd.reg_str())
    print_stdout(snippet.asm())


def gen_load_local_str(opd: Operand) -> None:
    name = opd.value
    off = off_of(name)

    snippet = copy_of(SnippetCollection.LOAD_STACK_ADDR)
    snippet.add_arg(modf_of(opd.var_type.kind))
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
        snippet.add_arg(modf_of(opd.var_type.kind))
        snippet.add_arg(f'-{off}')
        snippet.add_arg(opd.reg_str())
        print_stdout(snippet.asm())
    else:
        snippet = copy_of(SnippetCollection.LOAD_DATA_VAR)
        snippet.add_arg(modf_of(opd.var_type.kind))
        snippet.add_arg(name)
        snippet.add_arg(opd.reg_str())
        print_stdout(snippet.asm())


def gen_load_ptr(opd: Operand, vtype: VariableType = default_type):
    if opd.value not in Def.ptr_map:
        print_error('gen_load_ptr', f'No such pointer {opd.value}')

    # ? Placeholder
    tmp = copy_of(opd)
    tmp.var_type = vtype

    deref_snippet = bin_snippet(SnippetCollection.DEREF_REG, tmp, opd)
    print_stdout(deref_snippet.asm())


def gen_load_addr(opd: Operand):
    name = opd.value
    off = off_of(name)

    # if off > 0:
    #     off_opd = Operand(off, default_type, imm=True)
    #     off_opd.reg = alloc_reg(opd=off_opd)
    #     snippet = bin_snippet(SnippetCollection.ADD_OP, opd, off_opd)
    #     print_stdout(snippet.asm())

    snippet = copy_of(SnippetCollection.LOAD_STACK_ADDR)
    snippet.add_arg(modf_of(opd.var_type.kind))
    snippet.add_arg(f'-{off}')
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
        if vtype == ptr_type:
            gen_load_str_lit(opd)
        else:
            gen_load_imm(opd)

    else:
        if vtype.meta_kind == VariableMetaKind.PRIM:
            gen_load_var(opd)
        elif vtype == arr_type:
            gen_load_addr(opd)
        elif vtype == ptr_type:
            gen_load_addr(opd)
            gen_load_ptr(opd)
        else:
            print_error('gen_load', f'Invalid operand type {opd.var_type}')


def gen_write(opd: Operand, opd2: Operand):
    vtype = opd.var_type

    if vtype.meta_kind == VariableMetaKind.PRIM:
        gen_write_var(opd)
    elif vtype in (arr_type, ptr_type):
        gen_write_ref(opd, opd2)
    else:
        print_error('gen_write', f'Invalid operand type {opd.var_type}')


def gen_write_var(opd: Operand):
    name = opd.value
    off = off_of(name)

    # ? Fix for function parameters
    kind = opd.var_type.kind
    var = Def.var_map.get(name)
    is_ptr = Def.ident_map.get(name) == VariableMetaKind.PTR

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
    if is_acc and vtype == ptr_type:
        vtype = Def.ptr_map[left_opd.value].elem_type
    if is_acc and vtype == arr_type:
        vtype = Def.arr_map[left_opd.value].elem_type

    opd = copy_of(right_opd)
    opd.var_type = vtype

    snippet = copy_of(SnippetCollection.WRITEREF_REG)
    snippet.add_arg(modf_of(vtype.kind))
    snippet.add_arg(opd.reg_str())
    snippet.add_arg(left_opd.reg_str())
    print_stdout(snippet.asm())


def gen_widen(opd: Operand, var_type: VariableType):
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
    alloc_reg(Register.rax)
    for reg in CALL_REGS:
        alloc_reg(reg)

    reg_cnt = -1
    glue_node = node.left
    while glue_node is not None:
        reg_cnt += 1
        glue_node = glue_node.left

    glue_node = node.left

    # Fix for single-argument functions
    if glue_node.kind != NodeKind.GLUE:
        opd = gen_tree(glue_node, node, -1)
        opd_dst = Operand('', opd.var_type, CALL_REGS[0])

        gen_load(opd)

        snippet = copy_of(SnippetCollection.MOVE_REG)
        snippet.add_arg(modf_of(opd.var_type.kind))
        snippet.add_arg(opd.reg_str())
        snippet.add_arg(opd_dst.reg_str())
        print_stdout(snippet.asm())

        free_reg(opd.reg)
        free_reg(opd_dst.reg)

    else:
        while glue_node is not None:
            opd = gen_tree(glue_node.right, glue_node, -1)
            opd_dst = Operand('', opd.var_type, CALL_REGS[reg_cnt])

            gen_load(opd)
            # gen_load(opd_dst)

            snippet = copy_of(SnippetCollection.MOVE_REG)
            snippet.add_arg(modf_of(opd.var_type.kind))
            snippet.add_arg(opd.reg_str())
            snippet.add_arg(opd_dst.reg_str())
            print_stdout(snippet.asm())

            free_reg(opd.reg)
            free_reg(opd_dst.reg)

            glue_node = glue_node.left
            reg_cnt -= 1

    name = node.value
    fun = Def.fun_map.get(name)
    if fun.is_variadic:
        snippet = copy_of(SnippetCollection.XOR_RAX)
        print_stdout(snippet.asm())

    snippet = copy_of(SnippetCollection.CALL)
    snippet.add_arg(node.value)
    print_stdout(snippet.asm())

    for reg in CALL_REGS:
        free_reg(reg)

    return Operand('', default_type, Register.rax, True)


# TODO: Replace the print with a snippet.
def gen_sub_stack(off: int):
    print_stdout(f'sub ${off}, %rsp')


def bin_snippet(snippet_base: Snippet, left_opd: Operand, right_opd: Operand):
    '''
    left_opd: src
    right_opd: dest
    '''

    snippet = copy_of(snippet_base)
    snippet.add_arg(modf_of(left_opd.var_type.kind))
    snippet.add_arg(right_opd.reg_str())
    snippet.add_arg(left_opd.reg_str())

    return snippet


def gen_preamble():
    '''
    Unused.
    '''
    pass


def gen_postamble():

    def is_fun(item):
        _, value = item
        return value == VariableMetaKind.FUN

    funcs = list(filter(is_fun, Def.ident_map.items()))

    print_stdout()
    for fun_name, _ in funcs:
        fun = Def.fun_map.get(fun_name)
        if fun.is_extern:
            print_stdout(f'.extern {fun_name}')
        else:
            print_stdout(f'.global {fun_name}')
    print_stdout()

    print_stdout('.data')
    for (string, label) in Def.str_lit_map.items():
        print_stdout(f'{label}: .asciz \"{string}\"')

    for (name, var) in Def.var_map.items():
        if not var.is_local:
            print_stdout(f'{name}: {global_modf_of(var.vtype.kind)} 0')


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


def node_is_cmp(kind: NodeKind) -> bool:
    return kind in (
        NodeKind.OP_EQ,
        NodeKind.OP_NEQ,
        NodeKind.OP_GT,
        NodeKind.OP_LT,
        NodeKind.OP_GTE,
        NodeKind.OP_LTE
    )


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

    if Def.comments_enabled == True and node.kind in (NodeKind.OP_ASSIGN,
                                                      NodeKind.IF,
                                                      NodeKind.WHILE,
                                                      NodeKind.RET,
                                                      NodeKind.FUN,
                                                      NodeKind.FUN_CALL):
        # Local function variable
        if node.kind == NodeKind.FUN:
            for name, meta_kind in Def.ident_map.items():
                if name.startswith(node.value) and meta_kind != VariableMetaKind.FUN:
                    snippet = copy_of(SnippetCollection.CMT)
                    snippet.add_arg(f'{name}: -{off_of(name)}(%rbp)')
                    print_stdout(snippet.asm())

        body = GenStr.tree_str(node)
        for line in body.split('\n'):
            snippet = copy_of(SnippetCollection.CMT)
            snippet.add_arg(line)
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
        free_all_regs()
        return None

    if node.kind == NodeKind.FUN_CALL:
        return gen_fun_call(node)

    # Glue statement
    if node.kind == NodeKind.GLUE:
        gen_tree(node.left, node, -1)
        free_all_regs()
        gen_tree(node.right, node, -1)
        free_all_regs()
        return None

    if (node.left != None):
        left_opd = gen_tree(node.left, node, -1)
    if (node.right != None):
        right_opd = gen_tree(node.right, node, -1)

    if node.kind == NodeKind.OP_WIDEN:
        gen_load(left_opd)
        gen_widen(left_opd, node.ntype)
        return left_opd

    if node.kind == NodeKind.INT_LIT:
        opd = Operand(node.value, node.ntype, imm=True)
        opd.reg = alloc_reg(opd=opd)
        return opd

    if node.kind == NodeKind.CHAR_LIT:
        value = node.value.lstrip('\'').rstrip('\'')
        opd = Operand(ord(value), node.ntype, imm=True)
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
        opd = copy_of(left_opd)
        opd.value = node.left.value
        return opd

    # Dereference
    if node.kind == NodeKind.DEREF:
        if node != parent.left or parent.kind != NodeKind.OP_ASSIGN:
            ptr = Def.ptr_map.get(left_opd.value)
            elem_type = ptr.elem_type
            gen_load(left_opd)
            gen_load_ptr(left_opd, elem_type)
            left_opd.var_type = elem_type
            # !BUG: Widen
        return left_opd

    # Array access
    if node.kind == NodeKind.ARR_ACC:
        gen_load(left_opd)
        gen_load(right_opd)
        opd = Operand(size_of(right_opd.var_type),
                      right_opd.var_type, imm=True)
        opd.reg = alloc_reg(opd=opd)
        gen_load(opd)

        mul_snippet = bin_snippet(SnippetCollection.MUL_OP, opd, right_opd)
        add_snippet = bin_snippet(
            SnippetCollection.ADD_OP, left_opd, opd)
        print_stdout(mul_snippet.asm())
        print_stdout(add_snippet.asm())

        if node != parent.left or parent.kind != NodeKind.OP_ASSIGN:
            gen_load_ptr(left_opd)

        free_reg(right_opd.reg)
        free_reg(opd.reg)
        return left_opd

    # Assignment
    if node.kind == NodeKind.OP_ASSIGN:
        gen_load(right_opd)
        opd = copy_of(left_opd)
        if opd.var_type in (arr_type, ptr_type):
            if opd.reg == Register.id_max:
                opd.reg = alloc_reg(opd=opd)

            if node.left.kind != NodeKind.ARR_ACC:
                gen_load_addr(opd)

            is_deref = node.left.kind in (NodeKind.DEREF,
                                          NodeKind.ARR_ACC)
            # if is_deref:
            #     gen_load_ptr(opd)
            gen_write_ref(opd, right_opd, is_acc=is_deref)
        else:
            opd.reg = right_opd.reg
            gen_write_var(opd)

        return opd

    # Loading (phase 2)
    gen_load(left_opd)
    gen_load(right_opd)

    # Addition
    if (node.kind == NodeKind.OP_ADD):
        snippet = bin_snippet(SnippetCollection.ADD_OP, left_opd, right_opd)
        free_reg(right_opd.reg)
        print_stdout(snippet.asm())
        return left_opd

    # Subtraction
    if (node.kind == NodeKind.OP_SUB):
        snippet = bin_snippet(SnippetCollection.SUB_OP, left_opd, right_opd)
        free_reg(right_opd.reg)
        print_stdout(snippet.asm())
        return left_opd

    # Multiplication
    if node.kind == NodeKind.OP_MULT:
        if left_opd.reg != Register.rax:
            if right_opd.reg == Register.rax:
                left_opd, right_opd = right_opd, left_opd
            else:
                print_error('gen_tree', 'Multiplication error')

        snippet = bin_snippet(SnippetCollection.MUL_OP, left_opd, right_opd)
        print_stdout(snippet.asm())
        free_reg(right_opd.reg)
        return left_opd

    # Division/Modulo
    if node.kind in (NodeKind.OP_DIV, NodeKind.OP_MOD):
        in_reg = Register.rax
        out_reg = Register.rax if node.kind == NodeKind.OP_DIV else Register.rdx
        new_opd = gen_reg_chown(out_reg, left_opd, right_opd)
        old_opd = left_opd

        # left_opd.reg => rax (in)
        # right_opd.reg => reg (div)

        #! Duplicated code block
        if right_opd.reg == in_reg:
            kind = left_opd.var_type.kind
            tmp = Operand('', left_opd.var_type)
            tmp.reg = alloc_reg(opd=tmp)

            snippet = copy_of(SnippetCollection.MOVE_REG)
            snippet.add_arg(modf_of(left_opd.var_type.kind))
            snippet.add_arg(left_opd.reg_str())
            snippet.add_arg(tmp.reg_str())
            print_stdout(snippet.asm())

            snippet = copy_of(SnippetCollection.MOVE_REG)
            snippet.add_arg(modf_of(kind))
            snippet.add_arg(right_opd.reg_str())
            snippet.add_arg(left_opd.reg_str())
            print_stdout(snippet.asm())

            snippet = copy_of(SnippetCollection.MOVE_REG)
            snippet.add_arg(modf_of(kind))
            snippet.add_arg(tmp.reg_str())
            snippet.add_arg(right_opd.reg_str())
            print_stdout(snippet.asm())

            free_reg(tmp.reg)

        if node.kind == NodeKind.OP_MOD and right_opd.reg == out_reg:
            kind = left_opd.var_type.kind
            tmp = Operand('', left_opd.var_type)
            tmp.reg = alloc_reg(opd=tmp)

            snippet = copy_of(SnippetCollection.MOVE_REG)
            snippet.add_arg(modf_of(left_opd.var_type.kind))
            snippet.add_arg(left_opd.reg_str())
            snippet.add_arg(tmp.reg_str())
            print_stdout(snippet.asm())

            snippet = copy_of(SnippetCollection.MOVE_REG)
            snippet.add_arg(modf_of(kind))
            snippet.add_arg(right_opd.reg_str())
            snippet.add_arg(left_opd.reg_str())
            print_stdout(snippet.asm())

            snippet = copy_of(SnippetCollection.MOVE_REG)
            snippet.add_arg(modf_of(kind))
            snippet.add_arg(tmp.reg_str())
            snippet.add_arg(right_opd.reg_str())
            print_stdout(snippet.asm())

            free_reg(tmp.reg)

        snippet = copy_of(SnippetCollection.XOR_RDX)
        print_stdout(snippet.asm())

        snippet = copy_of(SnippetCollection.DIV_MOD_OP)
        snippet.add_arg(old_opd.reg_str())
        print_stdout(snippet.asm())
        free_reg(old_opd.reg)

        return new_opd

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
