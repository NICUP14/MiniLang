import enum
from typing import List
from dataclasses import dataclass


class SnippetId(enum.Enum):
    CALL = 0
    LABEL = 1
    JMP = 2
    COND_JMP = 3
    SET_REG = 4
    CMP_REG = 5
    MOVE_REG = 6
    LOAD_IMM = 7
    LOAD_STACK_VAR = 8
    ADD_OP = 9
    SUB_OP = 10
    MUL_OP = 11
    DIV_MOD_OP = 12
    ASSIGN_OP = 13
    WRITE_STACK_VAR = 14
    FUN_PREAMBLE = 15
    FUN_POSTAMBLE = 16
    EXTEND_REG = 17
    LOAD_STACK_ADDR = 18
    LOAD_DATA_ADDR = 19
    WRITEREF_REG = 20
    DEREF_REG = 21
    XOR_RAX = 22
    LOAD_DATA_VAR = 23


@dataclass
class Snippet:
    id: SnippetId
    fmt: str
    args: List[str]

    def add_arg(self, arg: str):
        self.args.append(arg)
        return self

    def asm(self):
        return self.fmt.format(*self.args)


class SnippetCollection:
    CALL = Snippet(SnippetId.CALL,
                   'call {}', [])

    LABEL = Snippet(SnippetId.LABEL,
                    'L{}:', [])

    JMP = Snippet(SnippetId.JMP,
                  'jmp L{}', [])

    COND_JMP = Snippet(SnippetId.COND_JMP,
                       'j{} L{}', [])

    SET_REG = Snippet(SnippetId.SET_REG,
                      'set{} {}', [])

    CMP_REG = Snippet(SnippetId.CMP_REG,
                      'cmp {}, {}', [])

    MOVE_REG = Snippet(SnippetId.MOVE_REG,
                       'mov{} {}, {}', [])

    EXTEND_REG = Snippet(SnippetId.EXTEND_REG,
                         'movsx {}, {}', [])

    WRITEREF_REG = Snippet(SnippetId.WRITEREF_REG,
                           'mov{} {}, ({})', [])

    DEREF_REG = Snippet(SnippetId.DEREF_REG,
                        'mov{} ({}), {}', [])

    LOAD_STACK_ADDR = Snippet(SnippetId.LOAD_STACK_ADDR,
                              'lea{} {}(%rbp), {}', [])

    LOAD_DATA_ADDR = Snippet(SnippetId.LOAD_DATA_ADDR,
                             'lea{} {}(%rip), {}', [])

    LOAD_DATA_VAR = Snippet(SnippetId.LOAD_DATA_VAR,
                            'mov{} {}(%rip), {}', [])

    LOAD_IMM = Snippet(SnippetId.LOAD_IMM,
                       'mov{} ${}, {}', [])

    LOAD_STACK_VAR = Snippet(SnippetId.LOAD_STACK_VAR,
                             'mov{} {}(%rbp), {}', [])

    WRITE_STACK_VAR = Snippet(SnippetId.WRITE_STACK_VAR,
                              'mov{} {}, {}(%rbp)', [])

    ADD_OP = Snippet(SnippetId.ADD_OP,
                     'add{} {}, {}', [])

    SUB_OP = Snippet(SnippetId.SUB_OP,
                     'sub{} {}, {}', [])

    MUL_OP = Snippet(SnippetId.MUL_OP,
                     'imul{} {}, {}', [])

    DIV_MOD_OP = Snippet(SnippetId.DIV_MOD_OP,
                         'idiv {}', [])

    FUN_PREAMBLE = Snippet(SnippetId.FUN_PREAMBLE,
                           '{}:\npush %rbp\nmov %rsp, %rbp', [])

    FUN_POSTAMBLE = Snippet(SnippetId.FUN_POSTAMBLE,
                            'leave\nret', [])

    XOR_RAX = Snippet(SnippetId.XOR_RAX,
                      'xor %rax, %rax', [])
