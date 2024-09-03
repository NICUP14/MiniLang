import Def
import copy
from Def import Node
from Def import NodeKind
from Def import print_error
from typing import List


def has_indent(kind: NodeKind):
    return kind in (
        NodeKind.IF,
        NodeKind.WHILE,
        NodeKind.FUN,
        NodeKind.STRUCT_DECL,
        # NodeKind.BLOCK,
        # NodeKind.NAMESPACE,
    )


def fun_call_tree_str(node: Node, func):
    if node.kind == NodeKind.FUN_CALL:
        name = node.value
        fun = Def.fun_map.get(name)
        if fun.arg_cnt == 0:
            return ''

    args = []
    glue_node = node.left

    # Fix for single-argument functions
    if glue_node.kind != NodeKind.GLUE:
        args.append(func(glue_node))

    else:
        while glue_node is not None:
            args.append(func(glue_node.right))
            glue_node = glue_node.left

    for arg in args:
        if arg is None:
            print_error('fun_call_tree_str',
                        f'Internal error in {node.value}\'s function call (args={func(node.left)})')

    args.reverse()
    return ', '.join(args)


class Walker:
    def __init__(self, step) -> None:
        self.step = step

    def walk(self, node: Node):
        return self.__walk(node)

    def __walk(self, node: Node, parent: Node = None, indent: int = 0):
        left = None
        right = None
        middle = None

        if node is None:
            return None

        if node.middle:
            middle = self.__walk(node.middle, node, indent)
        if node.kind != NodeKind.FUN_CALL and node.left:
            left = self.__walk(node.left, node, indent +
                               has_indent(node.left.kind) - (node.kind == NodeKind.END))
        if node.kind != NodeKind.FUN_CALL and node.right:
            right = self.__walk(node.right, node, indent +
                                has_indent(node.right.kind) - (node.kind == NodeKind.END))

        return self.step(node, parent, left, right, middle, indent)
