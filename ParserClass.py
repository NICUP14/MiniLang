import Def
from typing import Optional
from typing import List
from typing import Tuple
from Lexer import Token
from Lexer import TokenKind
from Lexer import tokenize
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
from Def import VariableType
from Def import VariableKind
from Def import VariableMetaKind
from Def import Function
from Def import Array
from Def import Pointer
from Def import String
from Def import ptr_type
from Def import arr_type
from Def import void_type
from Def import default_type
from Def import bool_type
from Def import print_error
from Def import type_of
from Def import type_of_op
from Def import type_of_ident
from Def import type_of_lit
from Def import full_name_of
from Def import needs_widen
from Def import allowed_op
from Def import size_of

PRECEDENCE_MAP = {
    TokenKind.DEREF: 26,
    TokenKind.AMP: 26,
    TokenKind.FUN_CALL: 25,
    TokenKind.PLUS: 10,
    TokenKind.MINUS: 10,
    TokenKind.MULT: 20,
    TokenKind.DIV: 20,
    TokenKind.PERC: 7,
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
    TokenKind.STR_LIT: NodeKind.STR_LIT
}


class Parser:
    def __init__(self) -> None:
        self.in_file = ''
        self.lines = []
        self.lines_idx = 0
        self.tokens = []
        self.tokens_idx = 0

    def parse(self, source: str) -> Node:
        self.source = source
        self.lines = list(filter(
            lambda l: l.lstrip('\t ') != '\n' and not l.lstrip('\t ').startswith('#'), open(source, 'r').readlines()))
        self.tokens = tokenize(self.curr_line())
        return self.compound_statement()

    def no_more_lines(self) -> bool:
        return self.lines_idx >= len(self.lines)

    def curr_line(self) -> str:
        return self.lines[self.lines_idx]

    def next_line(self) -> str:
        self.lines_idx += 1

        if self.no_more_lines():
            print_error('next_line', 'No more lines in list', self)

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
                # Detects if the token is a function call (token correction)
                if Def.ident_map.get(token.value) == VariableMetaKind.FUN:
                    op_stack.append(Token(TokenKind.FUN_CALL, token.value))

                else:
                    postfix_tokens.append(token)

            elif token_is_paren(token.kind):
                if token.kind == TokenKind.LPAREN:
                    op_stack.append(token)

                if token.kind == TokenKind.RPAREN:
                    while len(op_stack) > 0 and op_stack[-1].kind != TokenKind.LPAREN:
                        postfix_tokens.append(op_stack.pop())
                    op_stack.pop()

            elif token_is_op(token.kind):
                # Handles Unary operator (token correction)
                op_token = token
                if prev_token is None or token_is_op(prev_token.kind) or prev_token.kind == TokenKind.LPAREN:
                    if token.kind == TokenKind.MULT:
                        op_token = Token(TokenKind.DEREF, '*')
                    elif token.kind == TokenKind.AMP:
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

    def to_tree(self, tokens: List[Token]) -> Node:
        node_stack = []

        for token in tokens:
            if token_is_param(token.kind):
                # Distinguishes between identifiers and literals
                if token.kind == TokenKind.IDENT:
                    full_name = full_name_of(token.value)
                    node_stack.append(
                        Node(self.node_kind_of(token.kind), type_of_ident(full_name), full_name))

                else:
                    kind = self.node_kind_of(token.kind)
                    node_stack.append(
                        Node(kind, type_of_lit(kind), token.value))

            if token_is_op(token.kind):
                if token_is_unary_op(token.kind):
                    node = node_stack.pop()
                    kind = self.node_kind_of(token.kind)

                    if kind != NodeKind.FUN_CALL and kind not in allowed_op(node.ntype):
                        print_error(
                            'to_tree', f'Incompatible type {node.ntype}', self)

                    node_stack.append(
                        Node(kind, node.ntype, token.value, node))

                elif token_is_bin_op(token.kind):
                    right = node_stack.pop()
                    left = node_stack.pop()

                    # Creates the initial parameter tree of a function call
                    if token.kind == TokenKind.COMMA and (
                            left.left is None or left.left.kind != NodeKind.GLUE):
                        node_stack.append(Node(NodeKind.GLUE, void_type, '', Node(
                            NodeKind.GLUE, void_type, '', None, left), right))

                    else:
                        # Widens the operands if necessary
                        code = needs_widen(left.ntype, right.ntype)
                        if code == 1 and kind != NodeKind.GLUE:
                            left = Node(NodeKind.OP_WIDEN,
                                        right.ntype, left.value, left)
                        if code == 2 and kind != NodeKind.GLUE:
                            right = Node(NodeKind.OP_WIDEN, left.ntype,
                                         right.value, right)

                        kind = self.node_kind_of(token.kind)
                        if kind not in allowed_op(left.ntype):
                            print_error('to_tree',
                                        f'to_tree: Incompatible types {kind} {left.ntype}, {right.ntype}', self)

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

    #! BUG: non-working import statement
    def import_statement(self) -> Optional[Node]:
        pass

    def while_statement(self) -> Optional[Node]:
        cond_node = self.token_list_to_tree()

        self.next_line()
        body = self.compound_statement()

        return Node(NodeKind.WHILE, void_type, '', cond_node, body)

    def if_statement(self) -> Optional[Node]:
        cond_node = self.token_list_to_tree()

        self.next_line()
        true_node = self.compound_statement()

        false_node = None
        if self.curr_token().kind == TokenKind.KW_ELSE:
            self.next_line()
            false_node = self.compound_statement()

        node = Node(NodeKind.IF, '', void_type,
                    true_node, false_node, cond_node)
        return node

    def ret_statement(self) -> Optional[Node]:
        if Def.fun_name == '':
            print_error('ret_statement',
                        'Cannot return from outside a function', self)

        fun = Def.fun_map.get(Def.fun_name)
        node = self.token_list_to_tree()

        if fun.ret_type == Def.void_type:
            print_error('ret_statement',
                        'Cannot return from a void function', self)

        if node.ntype != fun.ret_type:
            print_error('ret_statement',
                        'The return type differs from the function\'s', self)

        return Node(NodeKind.RET, node.ntype, '', node)

    def fun_declaration(self, is_extern: bool = False) -> Optional[Node]:
        # Needed for extern
        name = self.match_token(TokenKind.IDENT).value
        self.match_token(TokenKind.LPAREN)

        # Needed for extern
        arg_names = []
        arg_types = []
        elem_types = []
        while self.curr_token().kind not in (TokenKind.RPAREN, TokenKind.PER_FUN):
            arg_name = self.match_token(TokenKind.IDENT).value
            self.match_token(TokenKind.COLON)

            type_str = self.curr_token().value
            arg_type = type_of(type_str)
            elem_type = arg_type
            self.next_token()

            if not self.no_more_tokens() and self.curr_token().kind == TokenKind.MULT:
                self.next_token()
                arg_type = ptr_type

            if not self.no_more_tokens() and self.curr_token().kind not in (TokenKind.RPAREN, TokenKind.PER_FUN):
                self.match_token(TokenKind.COMMA)

            arg_names.append(arg_name)
            arg_types.append(arg_type)
            elem_types.append(elem_type)

        token = self.match_token_from((TokenKind.RPAREN, TokenKind.PER_FUN))
        is_variadic = token.kind == TokenKind.PER_FUN

        if is_variadic:
            self.match_token(TokenKind.RPAREN)
        self.match_token(TokenKind.COLON)

        # Needed for extern
        ret_type = type_of(self.curr_token().value)
        fun = Function(name, len(arg_types), arg_names,
                       arg_types, ret_type, 0, is_variadic, is_extern)

        Def.ident_map[name] = VariableMetaKind.FUN
        Def.fun_map[name] = fun

        if is_extern:
            return None

        Def.fun_name = name
        Def.label_list.append(name)
        Def.var_off = 8

        # ? Temporary
        for (arg_name, arg_type, elem_type) in zip(arg_names, arg_types, elem_types):
            meta_kind = arg_type.meta_kind
            Def.ident_map[full_name_of(arg_name)] = meta_kind

            if meta_kind == VariableMetaKind.PRIM:
                Def.var_map[full_name_of(arg_name)] = Variable(
                    arg_type, Def.var_off, True)
            if meta_kind == VariableMetaKind.PTR:
                Def.ptr_map[full_name_of(arg_name)] = Pointer(
                    full_name_of(arg_name), elem_type, Def.var_off)
            Def.var_off += size_of(arg_type)

        self.next_line()
        body = self.compound_statement()

        Def.fun_name = ''
        Def.label_list.pop()

        # Patch the stack offset
        off = Def.var_off
        align_off = 0 if off % 16 == 0 else 8 - (off % 8)
        fun.off = off + align_off

        return Node(NodeKind.FUN, default_type, name, body)

    def type_definition(self):
        # typedef uint = int8*
        alias = self.match_token(TokenKind.IDENT).value
        self.match_token(TokenKind.ASSIGN)
        type_str = self.curr_token().value

        self.next_token()
        meta_kind = VariableMetaKind.PRIM
        if not self.no_more_tokens() and self.curr_token().kind == TokenKind.MULT:
            meta_kind = VariableMetaKind.PTR

        # ! Bug in type_of for ptr types.
        vtype = type_of(type_str, False)
        # print('DBG:', vtype, meta_kind)  # Debug
        Def.ident_map[alias] = meta_kind
        if meta_kind == VariableMetaKind.PRIM:
            Def.type_map[alias] = vtype
            Def.var_map[alias] = Variable(vtype, -1, True)
        if meta_kind == VariableMetaKind.PTR:
            Def.type_map[alias] = ptr_type
            Def.ptr_map[alias] = Pointer(alias, vtype, -1)

    def to_node(self, token: Token) -> Node:
        node = None
        kind = self.node_kind_of(token.kind)
        if token.kind != TokenKind.IDENT:
            node = Node(kind, type_of_lit(kind), token.value)
        else:
            full_name = full_name_of(token.value)
            node = Node(kind, type_of_ident(full_name), full_name)

        return node

    def array_elem_declaration(self, array: Node, elem: Node, idx: int) -> Node:
        idx_node = self.to_node(Token(TokenKind.INT_LIT, str(idx)))
        acc_node = Node(NodeKind.ARR_ACC, elem.ntype, '', array, idx_node)
        return Node(NodeKind.OP_ASSIGN, elem.ntype, '=', acc_node, elem)

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
                root = Node(NodeKind.GLUE, void_type, '', self.array_elem_declaration(
                    arr_node, node, idx), self.array_elem_declaration(arr_node, node2, idx + 1))
                idx += 2
            else:
                node = nodes.pop()
                root = Node(
                    NodeKind.GLUE, void_type, '', root, self.array_elem_declaration(arr_node, node, idx))
                idx += 1

        return root

    def declaration(self) -> Optional[Node]:
        name = self.match_token(TokenKind.IDENT).value
        self.match_token(TokenKind.COLON)

        var_type = type_of(self.curr_token().value)
        kind, meta_kind = var_type.kind, var_type.meta_kind
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

        var_type = VariableType(kind, meta_kind)
        if meta_kind == VariableMetaKind.ARR:
            var_type = arr_type
        if meta_kind == VariableMetaKind.PTR:
            var_type = ptr_type

        full_name = full_name_of(name)

        Def.ident_map[full_name] = meta_kind
        Def.var_off += size_of(var_type)

        if var_type.meta_kind == VariableMetaKind.PRIM:
            is_local = Def.fun_name != ''
            Def.var_map[full_name] = Variable(var_type, Def.var_off, is_local)

            self.match_token(TokenKind.ASSIGN)

            node = self.token_list_to_tree()

            if not is_local:
                return None

            return Node(NodeKind.OP_ASSIGN, var_type, '=', Node(NodeKind.IDENT, var_type, full_name), node)

        if var_type.meta_kind == VariableMetaKind.STR:
            Def.str_map[full_name] = String(
                full_name, Def.var_off)

            self.match_token(TokenKind.ASSIGN)

            node = self.token_list_to_tree()
            return Node(NodeKind.OP_ASSIGN, var_type, '=', Node(NodeKind.IDENT, var_type, full_name), node)

        if var_type.meta_kind == VariableMetaKind.ARR:
            elem_type = VariableType(var_type.kind, VariableMetaKind.PRIM)
            Def.arr_map[full_name] = Array(
                full_name, elem_cnt, elem_type, Def.var_off)
            Def.var_off += size_of(elem_type) * elem_cnt

            if self.no_more_tokens():
                return None

            self.match_token(TokenKind.ASSIGN)
            self.match_token(TokenKind.LBRACE)

            return self.array_declaration(full_name)

        if var_type.meta_kind == VariableMetaKind.PTR:
            elem_type = VariableType(kind, VariableMetaKind.PRIM)
            Def.ptr_map[full_name] = Pointer(full_name, elem_type, Def.var_off)

            self.match_token(TokenKind.ASSIGN)

            node = self.token_list_to_tree()
            return Node(NodeKind.OP_ASSIGN, var_type, '=', Node(NodeKind.IDENT, var_type, full_name), node)

        print_error('declaration',
                    f'Unknown meta kind {meta_kind}', self)
