import copy
import enum
from typing import List
from dataclasses import dataclass


class SnippetId(enum.Enum):
    CMT = enum.auto()
    CALL = enum.auto()
    LABEL = enum.auto()
    JMP = enum.auto()
    COND_JMP = enum.auto()
    SET_REG = enum.auto()
    CMP_REG = enum.auto()
    MOVE_REG = enum.auto()
    LOAD_IMM = enum.auto()
    LOAD_STACK_VAR = enum.auto()
    ADD_OP = enum.auto()
    SUB_OP = enum.auto()
    MUL_OP = enum.auto()
    DIV_MOD_OP = enum.auto()
    ASSIGN_OP = enum.auto()
    WRITE_STACK_VAR = enum.auto()
    FUN_PREAMBLE = enum.auto()
    FUN_POSTAMBLE = enum.auto()
    EXTEND_REG = enum.auto()
    LOAD_STACK_ADDR = enum.auto()
    LOAD_DATA_ADDR = enum.auto()
    WRITEREF_REG = enum.auto()
    DEREF_REG = enum.auto()
    XOR_RAX = enum.auto()
    LOAD_DATA_VAR = enum.auto()
    WRITE_DATA_VAR = enum.auto()
    XOR_RDX = enum.auto()


@dataclass
class Snippet:
    id: SnippetId
    fmt: str
    args: List[str]

    def add_arg(self, arg: str):
        self.args.append(str(arg))
        return self

    def asm(self):
        return self.fmt.format(*self.args)


class SnippetCollection:
    CMT = Snippet(SnippetId.CMT,
                  '# {}', [])

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

    WRITE_DATA_VAR = Snippet(SnippetId.WRITE_DATA_VAR,
                             'mov{} {}, {}(%rip)', [])

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

    XOR_RDX = Snippet(SnippetId.XOR_RDX,
                      'xor %rdx, %rdx', [])


def copy_of(snippet: Snippet) -> Snippet:
    return copy.deepcopy(snippet)
