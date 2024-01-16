from __future__ import annotations
import Def
from typing import Optional
from typing import List
from typing import Tuple
from os.path import exists
from Lexer import Token
from Lexer import TokenKind
from Lexer import tokenize
from Lexer import token_is_lit
from Lexer import token_is_param
from Lexer import token_is_op
from Lexer import token_is_paren
from Lexer import post_process
from Lexer import token_is_bin_op
from Lexer import token_is_unary_op
from Lexer import token_is_rassoc
from Def import Node
from Def import NodeKind
from Def import Variable
from Def import VariableCompKind
from Def import VariableType
from Def import VariableKind
from Def import VariableMetaKind
from Def import Function
from Def import Array
from Def import Pointer
from Def import Macro
from Def import bool_ckind
from Def import ptr_ckind
from Def import ref_ckind
from Def import arr_ckind
from Def import void_ckind
from Def import default_ckind
from Def import void_type
from Def import bool_type
from Def import default_type
from Def import str_type
from Def import print_error
from Def import type_of
from Def import type_of_op
from Def import type_of_ident
from Def import type_of_lit
from Def import full_name_of_var
from Def import full_name_of_fun
from Def import needs_widen
from Def import type_of_cast
from Def import allowed_op
from Def import size_of
from Def import rev_type_of
from Def import node_is_cmp
from Snippet import copy_of

PRECEDENCE_MAP = {
    TokenKind.DEREF: 26,
    TokenKind.AMP: 26,
    TokenKind.KW_ASM: 25,
    TokenKind.FUN_CALL: 25,
    TokenKind.MACRO_CALL: 26,
    TokenKind.PLUS: 10,
    TokenKind.MINUS: 10,
    TokenKind.MULT: 20,
    TokenKind.DIV: 20,
    TokenKind.PERC: 7,
    TokenKind.AND: 7,
    TokenKind.OR: 7,
    TokenKind.KW_AT: 27,
    TokenKind.ASSIGN: 4,
    TokenKind.EQ: 6,
    TokenKind.NEQ: 6,
    TokenKind.GT: 6,
    TokenKind.LT: 6,
    TokenKind.LTE: 6,
    TokenKind.GTE: 6,
    TokenKind.COMMA: 3
}

NODE_KIND_MAP = {
    TokenKind.INT_LIT: NodeKind.INT_LIT,
    TokenKind.CHAR_LIT: NodeKind.CHAR_LIT,
    TokenKind.PLUS: NodeKind.OP_ADD,
    TokenKind.MINUS: NodeKind.OP_SUB,
    TokenKind.MULT: NodeKind.OP_MULT,
    TokenKind.DIV: NodeKind.OP_DIV,
    TokenKind.PERC: NodeKind.OP_MOD,
    TokenKind.AND: NodeKind.OP_AND,
    TokenKind.OR: NodeKind.OP_OR,
    TokenKind.ASSIGN: NodeKind.OP_ASSIGN,
    TokenKind.EQ: NodeKind.OP_EQ,
    TokenKind.NEQ: NodeKind.OP_NEQ,
    TokenKind.LT: NodeKind.OP_LT,
    TokenKind.GT: NodeKind.OP_GT,
    TokenKind.LTE: NodeKind.OP_LTE,
    TokenKind.GTE: NodeKind.OP_GTE,
    TokenKind.IDENT: NodeKind.IDENT,
    TokenKind.COMMA: NodeKind.GLUE,
    TokenKind.KW_AT: NodeKind.ARR_ACC,
    TokenKind.DEREF: NodeKind.DEREF,
    TokenKind.AMP: NodeKind.REF,
    TokenKind.FUN_CALL: NodeKind.FUN_CALL,
    TokenKind.STR_LIT: NodeKind.STR_LIT,
    TokenKind.KW_ASM: NodeKind.ASM,
    TokenKind.KW_CAST: NodeKind.CAST,
    TokenKind.TRUE_LIT: NodeKind.TRUE_LIT,
    TokenKind.FALSE_LIT: NodeKind.FALSE_LIT
}


class Parser:
    def __init__(self, parser: Parser = None) -> None:
        if parser is not None:
            self.source = parser.source
            self.lineno = parser.lineno
            self.tokens = list(parser.tokens)
            self.tokens_idx = parser.tokens_idx
            self.lines = list(parser.lines)
            self.lines_idx = parser.lines_idx
        else:
            self.source = ''
            self.lineno = 0
            self.tokens = []
            self.tokens_idx = 0
            self.lines = []
            self.lines_idx = 0

    def parse(self, source: str = '') -> Node:
        if source != '':
            self.source = source
            self.lines = open(source, 'r').readlines()
        self.skip_blank_lines()

        self.tokens = tokenize(self.curr_line())
        return self.compound_statement()

    def no_more_lines(self) -> bool:
        return self.lines_idx >= len(self.lines)

    def curr_line(self) -> str:
        return self.lines[self.lines_idx]

    def skip_blank_lines(self) -> None:
        while self.curr_line().lstrip('\t ') == '\n' or self.curr_line().lstrip('\t ').startswith('#'):
            self.next_line()

    def next_line(self) -> str:
        self.lineno += 1
        self.lines_idx += 1

        if self.no_more_lines():
            print_error('next_line', 'No more lines in list', self)
        self.skip_blank_lines()

        self.tokens_idx = 0
        self.tokens = tokenize(self.curr_line())
        return self.curr_line()

    def no_more_tokens(self) -> bool:
        return self.tokens_idx >= len(self.tokens)

    def lookahead_token(self) -> Token:
        return self.tokens[self.tokens_idx + 1]

    def curr_token(self) -> Token:
        if self.no_more_tokens():
            print_error('curr_token', 'No more tokens in list.', self)

        return self.tokens[self.tokens_idx]

    def next_token(self) -> None:
        self.tokens_idx += 1

    def match_token(self, kind: TokenKind) -> Token:
        token = self.curr_token()

        if token.kind != kind:
            print_error('self.match_token',
                        f'Expected token kind {kind}, got {token.kind}', self)

        self.next_token()
        return token

    def match_token_from(self, kinds: Tuple[TokenKind]) -> Token:
        token = self.curr_token()

        if token.kind not in kinds:
            print_error('self.match_token_from',
                        f'Expected token kinds {kinds}, got {token.kind}', self)

        self.next_token()
        return token

    def token_list_to_tree(self) -> Node:
        return self.to_tree(self.to_postfix(post_process(self.tokens[self.tokens_idx:])))

    def node_kind_of(self, kind: TokenKind) -> NodeKind:
        if kind not in NODE_KIND_MAP:
            print_error('node_kind_of', f'Invalid token {kind}', self)

        return NODE_KIND_MAP.get(kind)

    def precedence_of(self, kind: TokenKind) -> int:
        if kind not in PRECEDENCE_MAP:
            print_error('precedence_of',
                        f'Expected operator, got {kind}', self)

        return PRECEDENCE_MAP.get(kind)

    def to_postfix(self, tokens: List[Token]) -> List[Token]:
        op_stack = []
        postfix_tokens = []
        prev_token = None

        def cmp_precedence(t, t2):
            return self.precedence_of(t.kind) <= self.precedence_of(t2.kind)

        for token in tokens:
            if token_is_param(token.kind):
                if token_is_lit(token.kind):
                    postfix_tokens.append(token)
                else:
                    # Detects if the token is a function/macro call (token correction)
                    fun_name = full_name_of_fun(
                        token.value, exhaustive_match=True)
                    if Def.ident_map.get(fun_name) == VariableMetaKind.MACRO:
                        op_stack.append(Token(TokenKind.MACRO_CALL, fun_name))

                    elif Def.ident_map.get(fun_name) == VariableMetaKind.FUN:
                        op_stack.append(Token(TokenKind.FUN_CALL, fun_name))

                    else:
                        name = full_name_of_var(
                            token.value, exhaustive_match=True)
                        if name not in Def.ident_map:
                            print_error('to_postfix',
                                        f'Invalid identifier {name}')

                        postfix_tokens.append(
                            Token(TokenKind.IDENT, name))

            elif token_is_paren(token.kind):
                if token.kind == TokenKind.LPAREN:
                    op_stack.append(token)

                if token.kind == TokenKind.RPAREN:
                    while len(op_stack) > 0 and op_stack[-1].kind != TokenKind.LPAREN:
                        postfix_tokens.append(op_stack.pop())
                    op_stack.pop()

            elif token_is_op(token.kind):
                # Assembly, offset, size, len, cast builtin pass-trough
                if token.kind in (TokenKind.KW_ASM, TokenKind.KW_OFF, TokenKind.KW_SIZE, TokenKind.KW_LEN, TokenKind.KW_CAST):
                    op_stack.append(token)
                    continue

                # Handles Unary operator (token correction)
                op_token = token
                if prev_token is None or token_is_op(prev_token.kind) or prev_token.kind == TokenKind.LPAREN:
                    if token.kind == TokenKind.MULT:
                        op_token = Token(TokenKind.DEREF, '*')
                    elif token.kind == TokenKind.AND:
                        op_token = Token(TokenKind.AMP, '&')
                    else:
                        print_error('to_postfix',
                                    f'Invalid unary operator kind {token.kind}', self)

                while len(op_stack) > 0 and (not token_is_rassoc(op_stack[-1].kind)) and op_stack[-1].kind != TokenKind.LPAREN and cmp_precedence(op_token, op_stack[-1]):
                    postfix_tokens.append(op_stack.pop())
                op_stack.append(op_token)

            else:
                print_error('to_postfix',
                            f'Invalid token kind {token.kind}', self)

            prev_token = token

        while len(op_stack) > 0:
            postfix_tokens.append(op_stack.pop())

        return postfix_tokens

    def cast_builtin(self, node: Node) -> Node:
        glue_node = node
        if node.left.kind != NodeKind.GLUE:
            print_error('cast_builtin',
                        'The cast builtin expects exactly 2 arguments, only one was provided', self)

        arg_cnt = 0
        args: list[Node] = []
        while glue_node is not None:
            arg_cnt += 1
            args.append(glue_node.right)
            glue_node = glue_node.left

        if arg_cnt != 2:
            print_error('cast_builtin',
                        f'The cast builtin expects exactly 2 parameters, {arg_cnt} were provided', self)

        str_node = args.pop()
        target_node = args.pop()

        if str_node is None or str_node.kind != NodeKind.STR_LIT:
            print_error('cast_builtin',
                        f'The first argument passed to the cast builtin is not a string literal, got {str_node.kind}', self)

        type_str = str_node.value.lstrip('\"').rstrip('\"')
        return Node(NodeKind.CAST, type_of_cast(type_str), 'cast', target_node)

    def args_to_list(self, node: Node) -> List[Node]:
        glue_node = node
        arg_list: list[Node] = []

        if glue_node.kind != NodeKind.GLUE:
            arg_list.append(glue_node)
        else:
            while glue_node is not None:
                arg_list.append(glue_node.right)
                glue_node = glue_node.left

            arg_list.reverse()

        return arg_list

    def expand_macro(self, macro: Macro, arg_list: List[Node]) -> Optional[Node]:
        if len(arg_list) != len(macro.arg_names):
            print_error('expand_macro',
                        f'Macro {macro.name} accepts {len(macro.arg_names)} arguments, but {len(arg_list)} were provided', self)
        arg_names = list(
            map(lambda name: full_name_of_var(name, exhaustive_match=False), macro.arg_names))
        for name in arg_names:
            Def.ident_map[name] = VariableMetaKind.MACRO_ARG

        def expand_arg(node: Node) -> Optional[Node]:
            # if node is None:
            #     return node
            if node is None or node.kind != NodeKind.IDENT:
                return node

            name = node.value
            if name not in arg_names:
                return node

            return arg_list[arg_names.index(name)]

        def helper(node: Node) -> Optional[Node]:
            if node is None:
                return None

            middle, left, right = list(
                map(lambda n: helper(expand_arg(n)), (node.middle, node.left, node.right)))

            return expand_arg(Node(node.kind, node.ntype, node.value, left, right, middle))

        macro.parser.lineno = self.lineno
        body = macro.parser.parse()
        self.lineno += (macro.parser.lineno - self.lineno - 1)

        # Removes macro placeholders
        Def.ident_map = dict(filter(lambda t: not t[0].startswith(
            f'{macro.name}_'), Def.ident_map.items()))

        return helper(body)

    def to_tree(self, tokens: List[Token]) -> Node:
        node_stack: list[Node] = []

        for token in tokens:
            if token_is_param(token.kind):
                # Lineno builtin
                if token.kind == TokenKind.KW_LINENO:
                    node_stack.append(
                        Node(NodeKind.INT_LIT, type_of_lit(NodeKind.INT_LIT), str(self.lineno + 1)))

                # Line builtin
                elif token.kind == TokenKind.KW_LINE:
                    chars = '\t '
                    newline = '\n'
                    node_stack.append(
                        Node(NodeKind.STR_LIT, type_of_lit(NodeKind.STR_LIT), f'"{self.curr_line().lstrip(chars).rstrip(newline)}"'))

                # Func builtin
                elif token.kind == TokenKind.KW_FUN:
                    node_stack.append(
                        Node(NodeKind.STR_LIT, type_of_lit(NodeKind.STR_LIT), f'"{Def.fun_name}"'))

                # File builtin
                elif token.kind == TokenKind.KW_FILE:
                    node_stack.append(
                        Node(NodeKind.STR_LIT, type_of_lit(NodeKind.STR_LIT), f'"{self.source}"'))

                # Distinguishes between identifiers and literals
                elif token.kind == TokenKind.IDENT:
                    print('DBG:', token.value)
                    node_stack.append(
                        Node(self.node_kind_of(token.kind), type_of_ident(token.value), token.value))

                else:
                    kind = self.node_kind_of(token.kind)
                    node_stack.append(
                        Node(kind, type_of_lit(kind), token.value))

            if token_is_op(token.kind):
                if token_is_unary_op(token.kind):
                    # Function call fix
                    if token.kind == TokenKind.FUN_CALL:
                        fun = Def.fun_map.get(token.value)
                        kind = self.node_kind_of(token.kind)

                        if fun.arg_cnt == 0:
                            node_stack.append(
                                Node(kind, fun.ret_type, token.value))
                        else:
                            if len(node_stack) == 0:
                                print_error('to_tree',
                                            'Missing function operand', self)
                            node = node_stack.pop()

                            node_stack.append(
                                Node(kind, fun.ret_type, token.value, node))
                        continue

                    if token.kind == TokenKind.MACRO_CALL:
                        macro = Def.macro_map.get(token.value)

                        if macro.arg_cnt == 0:
                            node_stack.append(self.expand_macro(macro, []))
                        else:
                            if len(node_stack) == 0:
                                print_error('to_tree',
                                            'Missing macro operand', self)

                            node = node_stack.pop()
                            body = self.expand_macro(
                                macro, self.args_to_list(node))

                            node_stack.append(body)

                        continue

                    if len(node_stack) == 0:
                        print_error('to_tree', 'Missing operand', self)
                    node = node_stack.pop()

                    # Offset builtin
                    if token.kind == TokenKind.KW_OFF:
                        if node.kind != NodeKind.STR_LIT:
                            print_error('to_tree',
                                        'The off_of builtin only accepts string literals')

                        off = Def.off_of(full_name_of_var(
                            node.value.lstrip('\"').rstrip('\"')))
                        node_stack.append(
                            Node(NodeKind.INT_LIT, type_of_lit(NodeKind.INT_LIT), str(off)))
                        continue

                    # Size builtin
                    if token.kind == TokenKind.KW_SIZE:
                        if node.kind != NodeKind.STR_LIT:
                            print_error('to_tree',
                                        'The size_of builtin only accepts string literals')

                        size = Def.size_of_ident(full_name_of_var(
                            node.value.lstrip('\"').rstrip('\"')))
                        node_stack.append(
                            Node(NodeKind.INT_LIT, type_of_lit(NodeKind.INT_LIT), str(size)))
                        continue

                    # Length builtin
                    if token.kind == TokenKind.KW_LEN:
                        if node.kind != NodeKind.STR_LIT:
                            print_error('to_tree',
                                        f'The len_of builtin only accepts string literals, got {node.kind}')

                        ident = full_name_of_var(
                            node.value.lstrip('\"').rstrip('\"'))
                        meta_kind = Def.ident_map.get(ident)
                        if ident not in Def.ident_map:
                            print_error('to_tree',
                                        'The len_of builtin only accepts pre-declared identifiers')
                        if meta_kind not in (VariableMetaKind.ARR, VariableMetaKind.PTR):
                            print_error('to_tree',
                                        'The len_of builtin only accepts array/pointer identifiers')

                        elem_cnt = 0
                        if meta_kind == VariableMetaKind.ARR:
                            arr = Def.arr_map.get(ident)
                            elem_cnt = arr.elem_cnt
                        if meta_kind == VariableMetaKind.PTR:
                            ptr = Def.ptr_map.get(ident)
                            elem_cnt = ptr.elem_cnt

                        node_stack.append(
                            Node(NodeKind.INT_LIT, type_of_lit(NodeKind.INT_LIT), str(elem_cnt)))
                        continue

                    # Cast builtin
                    if token.kind == TokenKind.KW_CAST:
                        node_stack.append(self.cast_builtin(node))
                        continue

                    kind = self.node_kind_of(token.kind)
                    if kind not in (NodeKind.ASM, NodeKind.FUN_CALL) and kind not in allowed_op(node.ntype.ckind):
                        print_error(
                            'to_tree', f'Incompatible type {node.ntype}', self)

                    op_type = type_of_op(kind, node.ntype)
                    if kind == NodeKind.DEREF and op_type == void_type:
                        print_error('to_tree',
                                    f'Cannot dereference the {node.value} pointer-to-void')

                    node_stack.append(
                        Node(kind, type_of_op(kind, node.ntype), token.value, node))

                elif token_is_bin_op(token.kind):
                    if len(node_stack) < 2:
                        print_error('to_tree', 'Missing operand', self)

                    right = node_stack.pop()
                    left = node_stack.pop()

                    # Validates fixed-index array acesses
                    if token.kind == TokenKind.KW_AT and right.kind == NodeKind.INT_LIT:
                        elem_cnt = 0
                        if Def.ident_map.get(left.value) == VariableMetaKind.PTR:
                            elem_cnt = Def.ptr_map.get(left.value).elem_cnt
                        elif Def.ident_map.get(left.value) == VariableMetaKind.ARR:
                            elem_cnt = Def.arr_map.get(left.value).elem_cnt
                        else:
                            print_error('to_tree',
                                        f'Invalid identifier {left.value}')

                        idx = int(right.value)
                        if elem_cnt > 0 and idx >= elem_cnt:
                            print_error('to_tree',
                                        f'Cannot access element at {idx} from {left.value}', self)

                    # Creates the initial parameter tree of a function call
                    if token.kind == TokenKind.COMMA and (
                            left.left is None or left.left.kind != NodeKind.GLUE):
                        node_stack.append(Node(NodeKind.GLUE, void_type, '', Node(
                            NodeKind.GLUE, void_type, '', None, left), right))

                    else:
                        # Widens the operands if necessary
                        code = needs_widen(left.ntype.ckind, right.ntype.ckind)
                        kind = self.node_kind_of(token.kind)
                        if code == 1 and kind not in (NodeKind.GLUE, NodeKind.OP_ASSIGN):
                            left = Node(NodeKind.OP_WIDEN,
                                        right.ntype, left.value, left)
                        if code == 2 and kind != NodeKind.GLUE:
                            right = Node(NodeKind.OP_WIDEN, left.ntype,
                                         right.value, right)

                        if kind != NodeKind.GLUE and (left.ntype == void_type or right.ntype == void_type):
                            print_error('to_tree',
                                        f'to_tree: Incompatible types {kind} {rev_type_of(left.ntype)}, {rev_type_of(right.ntype)}', self)

                        if kind not in allowed_op(left.ntype.ckind):
                            print_error('to_tree',
                                        f'to_tree: Incompatible types {kind} {rev_type_of(left.ntype)}, {rev_type_of(right.ntype)}', self)

                        node_stack.append(
                            Node(kind, type_of_op(kind), token.value, left, right))
                else:
                    print_error('to_tree',
                                f'Operator kind {token.kind} is neither binary or unary', self)

        return node_stack.pop()

    def statement(self) -> Optional[Node]:
        token = self.curr_token()
        if token.kind == TokenKind.KW_LET:
            self.next_token()
            return self.declaration()
        if token.kind == TokenKind.KW_IF:
            self.next_token()
            return self.if_statement()
        if token.kind == TokenKind.KW_WHILE:
            self.next_token()
            return self.while_statement()
        if token.kind == TokenKind.KW_FUN:
            self.next_token()
            return self.fun_declaration(is_extern=False)
        if token.kind == TokenKind.KW_RET:
            self.next_token()
            return self.ret_statement()
        if token.kind == TokenKind.KW_EXTERN:
            self.next_token()
            self.match_token(TokenKind.KW_FUN)
            return self.fun_declaration(is_extern=True)
        if token.kind == TokenKind.KW_TYPEDEF:
            self.next_token()
            return self.type_definition()
        if token.kind == TokenKind.KW_IMPORT:
            self.next_token()
            return self.import_statement()
        if token.kind == TokenKind.KW_NAMESPACE:
            self.next_token()
            return self.namespace_statement()
        if token.kind == TokenKind.KW_DEFER:
            self.next_token()
            return self.defer_statement()
        if token.kind == TokenKind.KW_BLOCK:
            self.next_token()
            return self.block_statement()
        if token.kind == TokenKind.KW_MACRO:
            self.next_token()
            return self.macro_statement()

        node = self.token_list_to_tree()
        return node

    def compound_statement(self) -> Optional[Node]:
        node = None
        while not self.no_more_lines() and self.curr_token().kind not in (TokenKind.KW_END, TokenKind.KW_ELSE):
            if node is None:
                node = self.statement()
            else:
                node = Node(NodeKind.GLUE, void_type,
                            '', node, self.statement())
            self.next_line()

        return node

    def import_statement(self) -> Optional[Node]:
        if Def.fun_name != '':
            print_error('import_statement',
                        'Local imports are not allowed', self)

        module = self.match_token(
            TokenKind.STR_LIT).value.lstrip('\"').rstrip('\"')
        module_source = f'{module}.ml'
        if not exists(module_source):
            print_error('import_statement',
                        f'Module \'{module_source}\' does not exist.', self)

        module_root = Parser().parse(module_source)
        return module_root

    def namespace_statement(self) -> Optional[Node]:
        if Def.fun_name != '':
            print_error('import_statement',
                        'Local namespaces are not allowed', self)

        namespace = self.match_token(TokenKind.IDENT).value
        self.next_line()

        Def.module_name_list.append(namespace)
        namespace_node = Node(NodeKind.NAMESPACE, void_type,
                              namespace, self.compound_statement())
        Def.module_name_list.pop()

        return Node(NodeKind.GLUE, void_type, '', namespace_node, Node(NodeKind.END, void_type, 'end'))

    def inject_cond(self, node: Node) -> Node:
        if node_is_cmp(node.kind):
            return node

        return Node(NodeKind.OP_EQ, bool_type, '==', node, Node(NodeKind.TRUE_LIT, bool_type, 'true'))

    def while_statement(self) -> Optional[Node]:
        cond_node = self.token_list_to_tree()
        if cond_node.ntype != bool_type:
            print_error('while_statement',
                        f'Expected a boolean expression, got type {rev_type_of(cond_node.ntype)}', self)

        self.next_line()
        cond_node = self.inject_cond(cond_node)
        body = self.compound_statement()

        node = Node(NodeKind.GLUE, void_type, '', Node(
            NodeKind.WHILE, void_type, '', cond_node, body), Node(NodeKind.END, void_type, 'end'))
        return node

    def if_statement(self) -> Optional[Node]:
        cond_node = self.token_list_to_tree()
        if cond_node.ntype != bool_type:
            print_error('if_statement',
                        f'Expected a boolean expression, got type {rev_type_of(cond_node.ntype)}', self)

        self.next_line()
        cond_node = self.inject_cond(cond_node)
        true_node = self.compound_statement()

        false_node = None
        if self.curr_token().kind == TokenKind.KW_ELSE:
            self.next_line()
            false_node = self.compound_statement()

        node = Node(NodeKind.GLUE, void_type, '', Node(NodeKind.IF, '', void_type,
                    true_node, false_node, cond_node), Node(NodeKind.END, void_type, 'end'))
        return node

    def ret_statement(self) -> Optional[Node]:
        if Def.fun_name == '':
            print_error('ret_statement',
                        'Cannot return from outside a function', self)

        fun = Def.fun_map.get(Def.fun_name)

        if fun.ret_type == Def.void_type:
            if not self.no_more_tokens():
                print_error('ret_statement',
                            'Cannot return a non-void value from a void function', self)

            return None
        else:
            node = self.token_list_to_tree()
            if node.ntype != fun.ret_type:
                print_error('ret_statement',
                            'The return type differs from the function\'s', self)

            node = Node(NodeKind.GLUE, void_type, '', Def.deferred,
                        Node(NodeKind.RET, node.ntype, '', node))
            return node

    def fun_declaration(self, is_extern: bool = False) -> Optional[Node]:
        if Def.fun_name != '':
            print_error('fun_declaration',
                        'Local functions are not allowed', self)

        # Needed for extern
        name = self.match_token(TokenKind.IDENT).value
        full_name = full_name_of_fun(name, force_global=True)
        self.match_token(TokenKind.LPAREN)

        # Needed for extern
        arg_names: list[str] = []
        arg_types: list[VariableType] = []
        elem_types: list[VariableType] = []
        elem_cnts: list[int] = []
        while self.curr_token().kind not in (TokenKind.RPAREN, TokenKind.PER_FUN):
            arg_name = self.match_token(TokenKind.IDENT).value
            self.match_token(TokenKind.COLON)

            type_str = self.curr_token().value
            arg_type = type_of(type_str)
            elem_type = arg_type
            elem_cnt = 0
            self.next_token()

            if not self.no_more_tokens() and self.curr_token().kind == TokenKind.AND:
                self.next_token()
                arg_type = VariableType(ref_ckind, arg_type.ckind)

            elif not self.no_more_tokens() and self.curr_token().kind == TokenKind.MULT:
                self.next_token()
                arg_type = VariableType(ptr_ckind, arg_type.ckind)

            elif not self.no_more_tokens() and self.curr_token().kind == TokenKind.LBRACE:
                self.next_token()
                arg_type = VariableType(ptr_ckind, arg_type.ckind)
                elem_cnt = int(self.match_token(TokenKind.INT_LIT).value)
                self.match_token(TokenKind.RBRACE)
                self.match_token(TokenKind.MULT)

            if not self.no_more_tokens() and self.curr_token().kind not in (TokenKind.RPAREN, TokenKind.PER_FUN):
                self.match_token(TokenKind.COMMA)

            arg_names.append(arg_name)
            arg_types.append(arg_type)
            elem_types.append(elem_type)
            elem_cnts.append(elem_cnt)

        token = self.match_token_from((TokenKind.RPAREN, TokenKind.PER_FUN))
        is_variadic = token.kind == TokenKind.PER_FUN

        if is_variadic:
            self.match_token(TokenKind.RPAREN)
        self.match_token(TokenKind.COLON)

        # Needed for extern
        ret_type = type_of(self.curr_token().value)
        self.next_token()

        if not self.no_more_tokens() and self.curr_token().kind == TokenKind.MULT:
            self.next_token()
            ret_type = VariableType(ptr_ckind, ret_type.ckind)

        if not self.no_more_tokens() and self.curr_token().kind == TokenKind.AND:
            self.next_token()
            ret_type = VariableType(ref_ckind, ret_type.ckind)

        if not self.no_more_tokens():
            print_error('fun_declaration',
                        'Junk after function declaration', self)

        fun = Function(full_name, len(arg_types), arg_names,
                       arg_types, ret_type, 0, is_variadic, is_extern)

        Def.ident_map[full_name] = VariableMetaKind.FUN
        Def.fun_map[full_name] = fun

        if is_extern:
            return None

        Def.block_cnt = 0
        Def.fun_name = full_name
        Def.fun_name_list.append(full_name)
        Def.var_off = 8

        # ? Temporary
        for (arg_name, arg_type, elem_type, elem_cnt) in zip(arg_names, arg_types, elem_types, elem_cnts):
            meta_kind = arg_type.meta_kind()
            Def.ident_map[full_name_of_var(
                arg_name, exhaustive_match=False)] = meta_kind

            Def.var_off += size_of(arg_type.ckind)
            if meta_kind == VariableMetaKind.PRIM:
                Def.var_map[full_name_of_var(arg_name)] = Variable(
                    arg_type, Def.var_off, True)
            if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF):
                Def.ptr_map[full_name_of_var(arg_name)] = Pointer(
                    full_name_of_var(arg_name), elem_cnt, elem_type, Def.var_off, meta_kind == VariableMetaKind.REF)

        self.next_line()
        body = self.compound_statement() if fun.ret_type != void_type else (
            Node(NodeKind.GLUE, void_type, '', self.compound_statement(), Def.deferred))

        Def.fun_name = ''
        Def.fun_name_list.pop()
        Def.deferred = None

        # Patch the stack offset
        off = Def.var_off
        align_off = 0 if off % 16 == 0 else 16 - (off % 16)
        fun.off = off + align_off

        node = Node(NodeKind.GLUE, void_type, '',
                    Node(NodeKind.FUN, default_ckind, full_name, body), Node(NodeKind.END, void_type, 'end'))
        return node

    def type_definition(self) -> None:
        alias = self.match_token(TokenKind.IDENT).value
        self.match_token(TokenKind.ASSIGN)
        type_str = self.curr_token().value

        self.next_token()
        meta_kind = VariableMetaKind.PRIM
        if not self.no_more_tokens() and self.curr_token().kind == TokenKind.MULT:
            meta_kind = VariableMetaKind.PTR

        vtype = type_of(type_str, False)
        if meta_kind == VariableMetaKind.PRIM:
            Def.ckind_map[alias] = vtype.ckind
        if meta_kind == VariableMetaKind.PTR:
            Def.ckind_map[alias] = ptr_ckind
        if meta_kind == VariableMetaKind.REF:
            Def.ckind_map[alias] = ref_ckind

    def defer_statement(self) -> None:
        node = self.token_list_to_tree()
        if Def.deferred is None:
            Def.deferred = node
        else:
            Def.deferred = Node(NodeKind.GLUE, void_type,
                                '', Def.deferred, node)

    def block_statement(self) -> Optional[Node]:
        name = ''
        unnamed_block = self.no_more_tokens()

        if unnamed_block:
            Def.block_cnt += 1
            name = f'block{Def.block_cnt}'
        else:
            name = self.match_token(TokenKind.IDENT).value

        self.next_line()
        scopeless_block = name.startswith('_')

        if not scopeless_block:
            Def.fun_name_list.append(name)
        block_node = Node(NodeKind.BLOCK, void_type,
                          name, self.compound_statement())
        if not scopeless_block:
            Def.fun_name_list.pop()

        return Node(NodeKind.GLUE, void_type, '', block_node, Node(NodeKind.END, void_type, 'end'))

    def macro_statement(self) -> None:
        if Def.fun_name != '':
            print_error('macro_declaration',
                        'Local macros are not allowed', self)

        full_name = full_name_of_fun(self.match_token(
            TokenKind.IDENT).value, exhaustive_match=False)
        self.match_token(TokenKind.LPAREN)

        arg_names: list[str] = []
        while self.curr_token().kind != TokenKind.RPAREN:
            arg_name = self.match_token(TokenKind.IDENT).value
            arg_names.append(full_name_of_var(
                arg_name, exhaustive_match=False))

            if not self.no_more_tokens() and self.curr_token().kind != TokenKind.RPAREN:
                self.match_token(TokenKind.COMMA)

        self.match_token(TokenKind.RPAREN)
        if not self.no_more_tokens():
            print_error('fun_declaration',
                        'Junk after macro declaration', self)
        self.next_line()
        Def.ident_map[full_name] = VariableMetaKind.MACRO
        Def.macro_map[full_name] = Macro(
            full_name, len(arg_names), arg_names, Parser(self))

        for name in arg_names:
            Def.ident_map[name] = VariableMetaKind.MACRO_ARG

        Def.macro_name = full_name
        _ = self.compound_statement()
        Def.macro_name = ''

        # Def.macro_name = full_name
        # Def.fun_name_list.append(full_name)
        # lines_idx_cpy = self.lines_idx
        # self.next_line()

        # # Hack for recursive macros (first-pass)
        # body = self.compound_statement()
        # Def.macro_map[full_name].body = body

        # # Rewind and re-read macro
        # self.lines_idx = lines_idx_cpy
        # self.next_line()

        # # Hack for self-calling macros (second-pass)
        # body = self.compound_statement()
        # Def.macro_map[full_name].body = body

        # Def.fun_name_list.pop()
        # Def.macro_name = ''

    def to_node(self, token: Token) -> Node:
        node = None
        kind = self.node_kind_of(token.kind)
        if token.kind != TokenKind.IDENT:
            node = Node(kind, type_of_lit(kind), token.value)
        else:
            full_name = full_name_of_var(token.value)
            node = Node(kind, type_of_ident(full_name), full_name)

        return node

    def array_elem_declaration(self, array: Node, elem: Node, idx: int) -> Node:
        idx_node = self.to_node(Token(TokenKind.INT_LIT, str(idx)))
        acc_node = Node(NodeKind.ARR_ACC, elem.ntype, '', array, idx_node)
        return Node(NodeKind.DECLARATION, elem.ntype, '=', acc_node, elem)

    def array_declaration(self, name: str) -> Node:
        root = None
        elems = []

        while self.curr_token().kind != TokenKind.RBRACE:
            token = self.match_token_from(
                (TokenKind.INT_LIT, TokenKind.CHAR_LIT, TokenKind.IDENT))

            if self.curr_token().kind != TokenKind.RBRACE:
                self.match_token(TokenKind.COMMA)

            elems.append(token)

        arr = Def.arr_map[name]
        if len(elems) > arr.elem_cnt:
            print_error('array_declaration',
                        f'Array {name} can only hold {arr.elem_cnt} elements', self)

        elems.reverse()
        nodes = list(map(self.to_node, elems))

        idx = 0
        arr_node = Node(NodeKind.IDENT, type_of_ident(name), name)

        if len(nodes) == 1:
            return self.array_elem_declaration(arr_node, nodes.pop(), 0)

        while len(nodes) > 0:
            if root is None:
                node = nodes.pop()
                node2 = nodes.pop()
                root = Node(NodeKind.GLUE, void_ckind, '', self.array_elem_declaration(
                    arr_node, node, idx), self.array_elem_declaration(arr_node, node2, idx + 1))
                idx += 2
            else:
                node = nodes.pop()
                root = Node(
                    NodeKind.GLUE, void_ckind, '', root, self.array_elem_declaration(arr_node, node, idx))
                idx += 1

        return root

    def heredoc_declaration(self):
        self.next_line()

        parts = []
        while not self.no_more_lines() and self.curr_token().kind != TokenKind.KW_END:
            parts.append(self.curr_line().lstrip('\t '))
            self.next_line()
        # self.next_line()

        value = ''.join(parts).rstrip('\n')
        return Node(NodeKind.STR_LIT, type_of_lit(NodeKind.STR_LIT), value)

    def declaration(self) -> Optional[Node]:
        name = self.match_token(TokenKind.IDENT).value

        is_implicit = self.curr_token().kind != TokenKind.COLON
        kind, meta_kind = VariableKind.INT64, VariableMetaKind.PRIM
        elem_kind, elem_meta_kind = VariableKind.INT64, VariableMetaKind.PRIM
        if not is_implicit:
            self.match_token(TokenKind.COLON)

            var_type = type_of(self.curr_token().value)
            kind, meta_kind = var_type.kind(), var_type.meta_kind()
            elem_kind, elem_meta_kind = kind, meta_kind
            self.next_token()

        elem_cnt = 0
        if not self.no_more_tokens() and self.curr_token().kind == TokenKind.LBRACE:
            self.next_token()

            meta_kind = VariableMetaKind.ARR
            elem_cnt = int(self.match_token(TokenKind.INT_LIT).value)
            self.match_token(TokenKind.RBRACE)

        if not self.no_more_tokens() and self.curr_token().kind == TokenKind.MULT:
            self.next_token()
            meta_kind = VariableMetaKind.PTR

        if not self.no_more_tokens() and self.curr_token().kind == TokenKind.AND:
            self.next_token()
            meta_kind = VariableMetaKind.REF

        if not self.no_more_tokens():
            self.match_token(TokenKind.ASSIGN)

        var_type = VariableType(VariableCompKind(kind, meta_kind))
        if is_implicit:
            if self.curr_token().kind == TokenKind.LBRACE:
                print_error(
                    'declaration',
                    'Implicit array declaration is not permitted.', self)

            node = self.token_list_to_tree()
            var_type = node.ntype
            if var_type.ckind == void_ckind:
                print_error('declaration',
                            'Declaration of implicit void primitive is not allowed.', self)

            kind, meta_kind = var_type.kind(), var_type.meta_kind()

            # Decays array to pointer
            if meta_kind == VariableMetaKind.ARR:
                meta_kind = VariableMetaKind.PTR
                elem_cnt = Def.arr_map.get(node.value).elem_cnt

            if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF):
                elem_kind = var_type.elem_ckind.kind
                elem_meta_kind = var_type.elem_ckind.meta_kind
        else:
            if meta_kind == VariableMetaKind.ARR:
                var_type = VariableType(arr_ckind, default_ckind)
            if meta_kind == VariableMetaKind.BOOL:
                var_type = VariableType(bool_ckind, default_ckind)
            if meta_kind == VariableMetaKind.PTR:
                var_type = VariableType(ptr_ckind, default_ckind)
            if meta_kind == VariableMetaKind.REF:
                var_type = VariableType(ref_ckind, default_ckind)

        # Fix for macros
        if Def.macro_name != '':
            # Placeholder identifier
            Def.ident_map[full_name_of_var(
                name, exhaustive_match=False)] = VariableMetaKind.MACRO_ARG
            return

        is_local = Def.fun_name != ''
        var_name = full_name_of_var(name, exhaustive_match=False)
        full_name = var_name if is_local else full_name_of_var(name, True)
        Def.ident_map[full_name] = meta_kind

        if meta_kind in (VariableMetaKind.PRIM, VariableMetaKind.BOOL):
            value = 0 if is_local else self.curr_token().value

            Def.var_off += size_of(var_type.ckind)
            Def.var_map[full_name] = Variable(
                var_type, Def.var_off, is_local, value)

            if not is_local:
                return None

            node = self.token_list_to_tree()
            if var_type == bool_type and var_type != node.ntype:
                print_error('declaration',
                            f'Incompatible assignment between types {rev_type_of(var_type)} and {rev_type_of(node.ntype)}')

            if node.ntype == void_ckind:
                print_error('declaration',
                            'Declaration of void primitive is not allowed.', self)

            return Node(NodeKind.DECLARATION, var_type, '=', Node(NodeKind.IDENT, var_type, full_name), node)

        if meta_kind == VariableMetaKind.ARR:
            elem_type = VariableType(VariableCompKind(
                kind, VariableMetaKind.PRIM))
            Def.var_off += size_of(elem_type.ckind) * elem_cnt
            Def.arr_map[full_name] = Array(
                full_name, elem_cnt, elem_type, Def.var_off)

            if self.no_more_tokens():
                return None

            self.match_token(TokenKind.LBRACE)

            return self.array_declaration(full_name)

        if meta_kind in (VariableMetaKind.PTR, VariableMetaKind.REF):
            elem_type = VariableType(
                VariableCompKind(elem_kind, elem_meta_kind))
            Def.var_off += size_of(var_type.ckind)
            Def.ptr_map[full_name] = Pointer(
                full_name, elem_cnt, elem_type, Def.var_off, meta_kind == VariableMetaKind.REF)

            node = None
            if self.curr_token().kind == TokenKind.HEREDOC:
                self.next_token()
                node = self.heredoc_declaration()
            else:
                node = self.token_list_to_tree()

            if node.ntype == void_type:
                print_error('declaration',
                            'Declaration of pointer with a void rvalue is not allowed.', self)

            return Node(NodeKind.DECLARATION, var_type, '=', Node(NodeKind.IDENT, var_type, full_name), node)

        print_error('declaration',
                    f'Unknown meta kind {meta_kind}', self)
