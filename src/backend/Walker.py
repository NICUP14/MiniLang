import Def
import copy
from Def import Node
from Def import NodeKind
from typing import List


def has_indent(kind: NodeKind):
    return kind in (
        NodeKind.IF,
        NodeKind.WHILE,
        NodeKind.FUN,
        NodeKind.BLOCK,
        NodeKind.NAMESPACE
    )


def args_to_list(node: Node) -> List[Node]:
    if node is None:
        return []

    glue_node = node
    arg_list: list[Node] = []
    if glue_node.kind != NodeKind.GLUE:
        arg_list.append(glue_node)
    else:
        # cnt = 0
        # while glue_node is not None:
        #     cnt += 1
        #     glue_node = glue_node.left

        # glue_node = node
        # if cnt > arg_cnt:
        #     block_node: Node = copy.deepcopy(node)
        #     arg_list.append(block_node)

        #     for _ in range(cnt - arg_cnt):
        #         block_node = block_node.left
        #     block_node.left = None

        #     for _ in range(cnt - arg_cnt + 1):
        #         glue_node = glue_node.left

        while glue_node is not None:
            arg_list.append(glue_node.right)
            glue_node = glue_node.left

        arg_list.reverse()

    return arg_list


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
