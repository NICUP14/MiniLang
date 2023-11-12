import copy
import Def
from Def import Node
from Def import NodeKind
from Def import Operand
from Def import Variable
from Def import VariableKind
from Def import VariableMetaKind
from Def import VariableType
from Def import Register
from Def import CALL_REGS
from Def import default_type
from Def import arr_type
from Def import ptr_type
from Def import alloc_reg
from Def import free_reg
from Def import free_all_regs
from Def import cmp_modf_of
from Def import modf_of
from Def import global_modf_of
from Def import size_of
from Def import off_of
from Snippet import SnippetCollection
import GenStr

label_idx = 0


def label() -> int:
    global label_idx
    curr_label = label_idx
    label_idx += 1

    return curr_label


def gen_label(label: int) -> None:
    snippet = copy.deepcopy(SnippetCollection.LABEL)
    snippet.add_arg(str(label))
    print(snippet.asm())


def gen_load_imm(opd: Operand) -> None:
    snippet = copy.deepcopy(SnippetCollection.LOAD_IMM)
    snippet.add_arg(modf_of(opd.var_type.kind))
    snippet.add_arg(opd.value)
    snippet.add_arg(opd.reg_str())
    print(snippet.asm())


def gen_load_str_lit(opd: Operand) -> None:
    snippet = copy.deepcopy(SnippetCollection.LOAD_DATA_ADDR)
    snippet.add_arg(modf_of(opd.var_type.kind))
    snippet.add_arg(opd.value)
    snippet.add_arg(opd.reg_str())
    print(snippet.asm())


def gen_load_local_str(opd: Operand) -> None:
    name = opd.value
    off = off_of(name)

    snippet = copy.deepcopy(SnippetCollection.LOAD_STACK_ADDR)
    snippet.add_arg(modf_of(opd.var_type.kind))
    snippet.add_arg(f'-{off}')
    snippet.add_arg(opd.reg_str())

    deref_snippet = bin_snippet(SnippetCollection.DEREF_REG, opd, opd)

    print(snippet.asm())
    print(deref_snippet.asm())


def gen_load_var(opd: Operand):
    name = opd.value
    off = off_of(name)

    var = Def.var_map[name]

    if var.is_local:
        snippet = copy.deepcopy(SnippetCollection.LOAD_STACK_VAR)
        snippet.add_arg(modf_of(opd.var_type.kind))
        snippet.add_arg(f'-{off}')
        snippet.add_arg(opd.reg_str())
        print(snippet.asm())
    else:
        snippet = copy.deepcopy(SnippetCollection.LOAD_DATA_VAR)
        snippet.add_arg(modf_of(opd.var_type.kind))
        snippet.add_arg(name)
        snippet.add_arg(opd.reg_str())
        print(snippet.asm())


def gen_load_ptr(opd: Operand):
    name = opd.value
    # off = off_of(name)

    deref_snippet = bin_snippet(SnippetCollection.DEREF_REG, opd, opd)

    print(deref_snippet.asm())


def gen_load_addr(opd: Operand):
    name = opd.value
    off = off_of(name)

    snippet = copy.deepcopy(SnippetCollection.LOAD_STACK_ADDR)
    snippet.add_arg(modf_of(opd.var_type.kind))
    snippet.add_arg(f'-{off}')
    snippet.add_arg(opd.reg_str())
    print(snippet.asm())


def gen_load(opd: Operand):
    if opd.is_loaded():
        return

    opd.load()
    if opd.reg == Register.id_max:
        opd.reg = alloc_reg()

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
            print(f'gen_load: Invalid operand type {opd.var_type}')
            exit(1)


def gen_write(opd: Operand, opd2: Operand):
    vtype = opd.var_type

    if vtype.meta_kind == VariableMetaKind.PRIM:
        gen_write_var(opd)
    elif vtype in (arr_type, ptr_type):
        gen_write_ref(opd, opd2)
    else:
        print(f'gen_write: Invalid operand type {opd.var_type}')
        exit(1)


def gen_write_var(opd: Operand):
    name = opd.value
    off = off_of(name)

    var = Def.var_map[name]

    if var.is_local:
        snippet = copy.deepcopy(SnippetCollection.WRITE_STACK_VAR)
        snippet.add_arg(modf_of(opd.var_type.kind))
        snippet.add_arg(opd.reg_str())
        snippet.add_arg(f'-{off}')
        print(snippet.asm())
    else:
        snippet = copy.deepcopy(SnippetCollection.WRITE_DATA_VAR)
        snippet.add_arg(modf_of(opd.var_type.kind))
        snippet.add_arg(opd.reg_str())
        snippet.add_arg(name)
        print(snippet.asm())


def gen_write_ref(left_opd: Operand, right_opd: Operand):
    snippet = copy.deepcopy(SnippetCollection.WRITEREF_REG)
    snippet.add_arg(modf_of(right_opd.var_type.kind))
    snippet.add_arg(right_opd.reg_str())
    snippet.add_arg(left_opd.reg_str())
    print(snippet.asm())


def gen_widen(opd: Operand, var_type: VariableType):
    opd2 = copy.deepcopy(opd)
    opd.var_type = var_type
    snippet = copy.deepcopy(SnippetCollection.EXTEND_REG)
    snippet.add_arg(opd2.reg_str())
    snippet.add_arg(opd.reg_str())
    print(snippet.asm())


def gen_if_tree(node: Node):
    false_label = label()
    end_label = label() if node.right else 0

    gen_tree(node.middle, node, false_label)
    free_all_regs()
    gen_tree(node.left, node, -1)
    free_all_regs()

    if node.right is not None:
        snippet = copy.deepcopy(SnippetCollection.JMP)
        snippet.add_arg(str(end_label))
        print(snippet.asm())

    snippet = copy.deepcopy(SnippetCollection.LABEL)
    snippet.add_arg(str(false_label))
    print(snippet.asm())

    if node.right is not None:
        gen_tree(node.right, node, -1)
        free_all_regs()

        snippet = copy.deepcopy(SnippetCollection.LABEL)
        snippet.add_arg(str(end_label))
        print(snippet.asm())


def gen_while_tree(node: Node):
    start_label = label()
    end_label = label()

    snippet = copy.deepcopy(SnippetCollection.LABEL)
    snippet.add_arg(str(start_label))
    print(snippet.asm())

    gen_tree(node.left, node, end_label)
    free_all_regs()
    gen_tree(node.right, node, -1)
    free_all_regs()

    jmp_snippet = copy.deepcopy(SnippetCollection.JMP)
    jmp_snippet.add_arg(str(start_label))
    print(jmp_snippet.asm())

    label_snippet = copy.deepcopy(SnippetCollection.LABEL)
    label_snippet.add_arg(str(end_label))
    print(label_snippet.asm())


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
        # gen_load(opd_dst)

        snippet = copy.deepcopy(SnippetCollection.MOVE_REG)
        snippet.add_arg(modf_of(opd.var_type.kind))
        snippet.add_arg(opd.reg_str())
        snippet.add_arg(opd_dst.reg_str())
        print(snippet.asm())

        free_reg(opd.reg)
        free_reg(opd_dst.reg)

    else:
        while glue_node is not None:
            opd = gen_tree(glue_node.right, glue_node, -1)
            opd_dst = Operand('', opd.var_type, CALL_REGS[reg_cnt])

            gen_load(opd)
            # gen_load(opd_dst)

            snippet = copy.deepcopy(SnippetCollection.MOVE_REG)
            snippet.add_arg(modf_of(opd.var_type.kind))
            snippet.add_arg(opd.reg_str())
            snippet.add_arg(opd_dst.reg_str())
            print(snippet.asm())

            free_reg(opd.reg)
            free_reg(opd_dst.reg)

            glue_node = glue_node.left
            reg_cnt -= 1

    # Temporarily disabled
    # print(SnippetCollection.XOR_RAX.asm())

    name = node.value
    fun = Def.fun_map.get(name)
    if fun.is_variadic:
        snippet = copy.deepcopy(SnippetCollection.XOR_RAX)
        print(snippet.asm())

    snippet = copy.deepcopy(SnippetCollection.CALL)
    snippet.add_arg(node.value)
    print(snippet.asm())

    for reg in CALL_REGS:
        free_reg(reg)

    return Operand('', default_type, Register.rax, True)


def gen_sub_stack(off: int):
    print(f'sub ${off}, %rsp')


def bin_snippet(snippet_base, left_opd: Operand, right_opd: Operand):
    snippet = copy.deepcopy(snippet_base)
    snippet.add_arg(modf_of(left_opd.var_type.kind))
    snippet.add_arg(right_opd.reg_str())
    snippet.add_arg(left_opd.reg_str())

    return snippet


def gen_preamble():
    print('.data')
    print('fmt: .asciz \"%d\\n\"')
    print('assert_num: .quad 0')
    print('errmsg: .asciz "Assert %d failed\\n"')
    print('.text')
    print('assert:')
    print('enter $0, $0')
    print('cmp $1, %dil')
    print('je LL1')
    print('lea errmsg(%rip), %rdi')
    print('mov assert_num(%rip), %rsi')
    print('xor %rax, %rax')
    print('call printf')
    print('mov $1, %rax')
    print('call exit')
    print('LL1:')
    print('addq $1, assert_num(%rip)')
    print('leave')
    print('ret')
    print('print:')
    print('enter $0, $0')
    print('mov %rdi, %rsi')
    print('lea fmt(%rip), %rdi')
    print('xor %rax, %rax')
    print('call printf')
    print('leave')
    print('ret')


def gen_postamble():

    def is_fun(item):
        _, value = item
        return value == VariableMetaKind.FUN

    funcs = list(filter(is_fun, Def.ident_map.items()))

    print()
    for fun_name, _ in funcs:
        fun = Def.fun_map.get(fun_name)
        if fun.is_extern:
            print(f'.extern {fun_name}')
        else:
            print(f'.global {fun_name}')
    print()

    print('.data')
    for (string, label) in Def.str_lit_map.items():
        print(f'{label}: .asciz \"{string}\"')

    for (name, var) in Def.var_map.items():
        if not var.is_local:
            print(f'{name}: {global_modf_of(var.vtype.kind)} 0')


def gen_fun_preamble(name: str):
    snippet = copy.deepcopy(SnippetCollection.FUN_PREAMBLE)
    snippet.add_arg(name)
    print(snippet.asm())

    fun = Def.fun_map.get(name)

    gen_sub_stack(fun.off)

    for arg_idx in range(fun.arg_cnt - 1, -1, -1):
        arg_name = f'{name}_{fun.arg_names[arg_idx]}'
        opd = Operand(arg_name,
                      fun.arg_types[arg_idx], CALL_REGS[arg_idx])
        gen_write_var(opd)


def gen_fun_postamble():
    snippet = copy.deepcopy(SnippetCollection.FUN_POSTAMBLE)
    print(snippet.asm())


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
        print(f'opposite_of: Invalid node kind {kind}')
        exit(1)

    return kind_map.get(kind)


def gen_tree(node: Node, parent: Node, curr_label: int):
    left_opd = None
    right_opd = None

    # ? Temporary
    # if node is None:
    #     print(f'gen_tree: Invalid call from parent {parent.kind}')
    #     exit(1)
    if node is None:
        return

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
        # gen_load(opd_dst)

        snippet = bin_snippet(SnippetCollection.MOVE_REG, opd_dst, opd)
        print(snippet.asm())
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
        opd = Operand(node.value, node.ntype, alloc_reg(), imm=True)
        return opd

    if node.kind == NodeKind.CHAR_LIT:
        value = node.value.lstrip('\'').rstrip('\'')
        opd = Operand(ord(value), node.ntype, alloc_reg(), imm=True)
        return opd

    if node.kind == NodeKind.STR_LIT:
        string = node.value.lstrip('\"').rstrip('\"')
        value = ""

        if string not in Def.str_lit_map:
            Def.str_lit_map[string] = f'str_{len(Def.str_lit_map)}'
        value = Def.str_lit_map.get(string)

        opd = Operand(value, node.ntype, alloc_reg(), imm=True)
        return opd

    if node.kind == NodeKind.IDENT:
        opd = Operand(node.value, node.ntype, Register.id_max)
        # if parent.kind in (NodeKind.GLUE, NodeKind.FUN_CALL, NodeKind.ARR_ACC, NodeKind.DEREF, NodeKind.REF) or (
        #    parent.right == node and parent.kind == NodeKind.OP_ASSIGN):
        #     opd.reg = alloc_reg()
        #     if opd.var_type == ptr_type:
        #         gen_load_addr(opd)
        #         gen_load_ptr(opd)
        #     if opd.var_type == arr_type:
        #         gen_load_addr(opd)
        #     if opd.var_type.meta_kind == VariableMetaKind.PRIM:
        #         gen_load_var(opd)
        return opd

    # Reference
    if node.kind == NodeKind.REF:
        opd = copy.deepcopy(left_opd)
        opd.value = node.left.value
        # gen_load(opd)
        # gen_load_addr(opd)
        return opd

    # Dereference
    if node.kind == NodeKind.DEREF:
        gen_load(left_opd)
        deref_snippet = bin_snippet(
            SnippetCollection.DEREF_REG, left_opd, left_opd)
        print(deref_snippet.asm())
        return left_opd

    # Array access
    if node.kind == NodeKind.ARR_ACC:
        opd = Operand(size_of(right_opd.var_type),
                      right_opd.var_type, alloc_reg())
        # if left_opd.var_type == arr_type:
        #     gen_load_addr(left_opd)
        # if left_opd.var_type == ptr_type:
        #     gen_load_ptr(left_opd)
        # gen_load_imm(opd)
        mul_snippet = bin_snippet(SnippetCollection.MUL_OP, opd, right_opd)
        add_snippet = bin_snippet(
            SnippetCollection.ADD_OP, left_opd, opd)
        print(mul_snippet.asm())
        print(add_snippet.asm())

        if node != parent.left or parent.kind != NodeKind.OP_ASSIGN:
            deref_snippet = bin_snippet(
                SnippetCollection.DEREF_REG, left_opd, left_opd)
            print(deref_snippet.asm())

        free_reg(right_opd.reg)
        return left_opd

    # Loading (phase 2)
    gen_load(left_opd)
    gen_load(right_opd)

    # Assignment
    if node.kind == NodeKind.OP_ASSIGN:
        opd = copy.deepcopy(left_opd)
        if opd.var_type in (arr_type, ptr_type):
            if opd.reg == Register.id_max:
                opd.reg = alloc_reg()
                gen_load_addr(opd)
                gen_write_ref(opd, right_opd)
        else:
            opd.reg = right_opd.reg
            gen_write_var(opd)

        return opd

    # Addition
    if (node.kind == NodeKind.OP_ADD):
        snippet = bin_snippet(SnippetCollection.ADD_OP, left_opd, right_opd)
        free_reg(right_opd.reg)
        print(snippet.asm())
        return left_opd

    # Subtraction
    if (node.kind == NodeKind.OP_SUB):
        snippet = bin_snippet(SnippetCollection.SUB_OP, left_opd, right_opd)
        free_reg(right_opd.reg)
        print(snippet.asm())
        return left_opd

    # Multiplication
    if node.kind == NodeKind.OP_MULT:
        if left_opd.reg != Register.rax:
            if right_opd.reg == Register.rax:
                left_opd, right_opd = right_opd, left_opd
            else:
                print('gen_tree: Multiplication error')
                exit(1)

        snippet = copy.deepcopy(SnippetCollection.MUL_OP)
        snippet.add_arg(right_opd.reg_str())
        print(snippet.asm())
        free_reg(right_opd.reg)
        return left_opd

    # Division/Modulo
    if node.kind in (NodeKind.OP_DIV, NodeKind.OP_MOD):
        out_reg = Register.rax if node.kind == NodeKind.OP_DIV else Register.rdx

        if out_reg not in (left_opd.reg, right_opd.reg):
            left_opd.reg = out_reg
            alloc_reg(out_reg)

        snippet = copy.deepcopy(SnippetCollection.XOR_RDX)
        print(snippet.asm())

        snippet = copy.deepcopy(SnippetCollection.DIV_MOD_OP)
        snippet.add_arg(right_opd.reg_str())
        print(snippet.asm())
        free_reg(right_opd.reg)

        left_opd.reg = out_reg
        return left_opd

    # Comparison
    if node_is_cmp(node.kind):
        cmp_snippet = copy.deepcopy(SnippetCollection.CMP_REG)
        cmp_snippet.add_arg(right_opd.reg_str())
        cmp_snippet.add_arg(left_opd.reg_str())
        print(cmp_snippet.asm())
        opd = copy.deepcopy(left_opd)
        opd.var_type = node.ntype

        if parent.kind not in (NodeKind.IF, NodeKind.WHILE):
            set_snippet = copy.deepcopy(SnippetCollection.SET_REG)
            set_snippet.add_arg(cmp_modf_of(node.kind))
            set_snippet.add_arg(opd.reg_str())
            print(set_snippet.asm())
        else:
            jmp_snippet = copy.deepcopy(SnippetCollection.COND_JMP)
            jmp_snippet.add_arg(cmp_modf_of(opposite_of(node.kind)))
            jmp_snippet.add_arg(str(curr_label))
            print(jmp_snippet.asm())

        free_reg(right_opd.reg)
        return opd

    print(f'gen_tree: Invalid node kind: {node.kind}')
    exit(1)
