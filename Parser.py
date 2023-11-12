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
from Def import type_of
from Def import type_of_op
from Def import type_of_ident
from Def import type_of_lit
from Def import full_name_of
from Def import needs_widen
from Def import allowed_op
from Def import size_of

parser_lines = []
parser_lines_idx = 0
parser_tokens = []
parser_tokens_idx = 0

PRECEDENCE_MAP = {
    TokenKind.DEREF: 26,
    TokenKind.AMP: 26,
    TokenKind.FUN_CALL: 25,
    TokenKind.PLUS: 10,
    TokenKind.MINUS: 10,
    TokenKind.MULT: 20,
    TokenKind.DIV: 20,
    TokenKind.PERC: 7,
    TokenKind.KW_AT: 5,
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


def no_more_lines() -> bool:
    return parser_lines_idx >= len(parser_lines)


def curr_line() -> str:
    return parser_lines[parser_lines_idx]


def next_line() -> str:
    global parser_tokens_idx
    global parser_tokens
    global parser_lines_idx
    parser_lines_idx += 1

    if no_more_lines():
        print('next_line: No more lines in list')
        exit(1)

    parser_tokens_idx = 0
    parser_tokens = tokenize(curr_line())
    return curr_line()


def no_more_tokens() -> bool:
    return parser_tokens_idx >= len(parser_tokens)


def lookahead_token() -> Token:
    return parser_tokens[parser_tokens_idx + 1]


def curr_token() -> Token:
    if no_more_tokens():
        print(f'{parser_lines_idx}: curr_token: No more tokens in list')
        exit(1)

    return parser_tokens[parser_tokens_idx]


def next_token() -> None:
    global parser_tokens_idx
    parser_tokens_idx += 1


def match_token(kind: TokenKind) -> Token:
    token = curr_token()

    if token.kind != kind:
        print(f'match_token: Expected token kind {kind}, got {token.kind}')
        exit(1)

    next_token()
    return token


def match_token_from(kinds: Tuple[TokenKind]) -> Token:
    token = curr_token()

    if token.kind not in kinds:
        print(
            f'match_token_from: Expected token kinds {kinds}, got {token.kind}')
        exit(1)

    next_token()
    return token


def token_list_to_tree() -> Node:
    return to_tree(to_postfix(post_process(parser_tokens[parser_tokens_idx:])))


def node_kind_of(kind: TokenKind) -> NodeKind:
    if kind not in NODE_KIND_MAP:
        print(f'node_kind_of: Invalid token {kind}')
        exit(1)

    return NODE_KIND_MAP.get(kind)


def precedence_of(kind: TokenKind) -> int:
    if kind not in PRECEDENCE_MAP:
        print(f'precedence_of: Expected operator, got {kind}')
        exit(1)

    return PRECEDENCE_MAP.get(kind)


def to_postfix(tokens: List[Token]) -> List[Token]:
    op_stack = []
    postfix_tokens = []
    prev_token = None

    def cmp_precedence(t, t2):
        return precedence_of(t.kind) <= precedence_of(t2.kind)

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
                    print(
                        f'to_postfix: Invalid unary operator kind {token.kind}')
                    exit(1)

            while len(op_stack) > 0 and (not token_is_rassoc(op_stack[-1].kind)) and op_stack[-1].kind != TokenKind.LPAREN and cmp_precedence(op_token, op_stack[-1]):
                postfix_tokens.append(op_stack.pop())
            op_stack.append(op_token)

        else:
            print(f'to_postfix: Invalid token kind {token.kind}')
            exit(1)

        prev_token = token

    while len(op_stack) > 0:
        postfix_tokens.append(op_stack.pop())

    return postfix_tokens


def to_tree(tokens: List[Token]) -> Node:
    node_stack = []

    for token in tokens:
        if token_is_param(token.kind):
            # Distinguishes between identifiers and literals
            if token.kind == TokenKind.IDENT:
                full_name = full_name_of(token.value)
                node_stack.append(
                    Node(node_kind_of(token.kind), type_of_ident(full_name), full_name))

            else:
                kind = node_kind_of(token.kind)
                node_stack.append(
                    Node(kind, type_of_lit(kind), token.value))

        if token_is_op(token.kind):
            if token_is_unary_op(token.kind):
                node = node_stack.pop()
                kind = node_kind_of(token.kind)

                if kind != NodeKind.FUN_CALL and kind not in allowed_op(node.ntype):
                    print(
                        f'to_tree: Incompatible type {node.ntype}')
                    exit(1)

                node_stack.append(Node(kind, node.ntype, token.value, node))

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

                    kind = node_kind_of(token.kind)
                    if kind not in allowed_op(left.ntype):
                        print(
                            f'to_tree: Incompatible types {left.ntype}, {right.ntype}')
                        exit(1)

                    node_stack.append(
                        Node(kind, type_of_op(kind), token.value, left, right))
            else:
                print(
                    f'to_tree: Operator kind {token.kind} is neither binary or unary')
                exit(1)

    return node_stack.pop()


def statement() -> Optional[Node]:
    token = curr_token()
    if token.kind == TokenKind.KW_LET:
        next_token()
        return declaration()
    if token.kind == TokenKind.KW_IF:
        next_token()
        return if_statement()
    if token.kind == TokenKind.KW_WHILE:
        next_token()
        return while_statement()
    if token.kind == TokenKind.KW_FUN:
        next_token()
        return fun_declaration(is_extern=False)
    if token.kind == TokenKind.KW_RET:
        next_token()
        return ret_statement()
    if token.kind == TokenKind.KW_EXTERN:
        next_token()
        match_token(TokenKind.KW_FUN)
        return fun_declaration(is_extern=True)

    node = token_list_to_tree()
    return node


def compund_statement() -> Optional[Node]:
    node = None
    while not no_more_lines() and curr_token().kind not in (TokenKind.KW_END, TokenKind.KW_ELSE):
        if node is None:
            node = statement()
        else:
            node = Node(NodeKind.GLUE, void_type, '', node, statement())
        next_line()

    return node


def while_statement() -> Optional[Node]:
    cond_node = token_list_to_tree()

    next_line()
    body = compund_statement()

    return Node(NodeKind.WHILE, void_type, '', cond_node, body)


def if_statement() -> Optional[Node]:
    cond_node = token_list_to_tree()

    next_line()
    true_node = compund_statement()

    false_node = None
    if curr_token().kind == TokenKind.KW_ELSE:
        next_line()
        false_node = compund_statement()

    node = Node(NodeKind.IF, '', void_type, true_node, false_node, cond_node)
    return node


def ret_statement() -> Optional[Node]:
    if Def.fun_name == '':
        print('ret_statement: Cannot return from outside a function')
        exit(1)

    fun = Def.fun_map.get(Def.fun_name)
    node = token_list_to_tree()

    if fun.ret_type == Def.void_type:
        print('ret_statement: Cannot return from a void function')
        exit(1)

    if node.ntype != fun.ret_type:
        print('ret_statement: The return type differs from the function\'s')
        exit(1)

    return Node(NodeKind.RET, node.ntype, '', node)


def fun_declaration(is_extern: bool = False) -> Optional[Node]:
    # Needed for extern
    name = match_token(TokenKind.IDENT).value
    match_token(TokenKind.LPAREN)

    # Needed for extern
    arg_names = []
    arg_types = []
    while curr_token().kind not in (TokenKind.RPAREN, TokenKind.PER_FUN):
        arg_name = match_token(TokenKind.IDENT).value
        match_token(TokenKind.COLON)

        type_str = curr_token().value
        next_token()

        if curr_token().kind not in (TokenKind.RPAREN, TokenKind.PER_FUN):
            match_token(TokenKind.COMMA)

        arg_names.append(arg_name)
        arg_types.append(type_of(type_str))

    token = match_token_from((TokenKind.RPAREN, TokenKind.PER_FUN))
    is_variadic = token.kind == TokenKind.PER_FUN

    if is_variadic:
        match_token(TokenKind.RPAREN)
    match_token(TokenKind.COLON)

    # Needed for extern
    ret_type = type_of(curr_token().value)
    fun = Function(name, len(arg_types), arg_names,
                   arg_types, ret_type, 0, is_variadic, is_extern)

    Def.ident_map[name] = VariableMetaKind.FUN
    Def.fun_map[name] = fun

    if is_extern:
        return None

    Def.fun_name = name
    Def.label_list.append(name)
    Def.var_off = 8

    for arg_idx, (arg_name, arg_type) in enumerate(zip(arg_names, arg_types)):
        Def.ident_map[full_name_of(arg_name)] = VariableMetaKind.PRIM
        Def.var_map[full_name_of(arg_name)] = Variable(
            arg_type, Def.var_off, True)
        Def.var_off += size_of(arg_type)

    next_line()
    body = compund_statement()

    Def.fun_name = ''
    Def.label_list.pop()

    # Patch the stack offset
    off = Def.var_off
    allign_off = 0 if off % 16 == 0 else 8 - (off % 8)
    fun.off = off + allign_off

    return Node(NodeKind.FUN, default_type, name, body)


def to_node(token: Token) -> Node:
    node = None
    kind = node_kind_of(token.kind)
    if token.kind != TokenKind.IDENT:
        node = Node(kind, type_of_lit(kind), token.value)
    else:
        full_name = full_name_of(token.value)
        node = Node(kind, type_of_ident(full_name), full_name)

    return node


def array_elem_declaration(array: Node, elem: Node, idx: int) -> Node:
    idx_node = to_node(Token(TokenKind.INT_LIT, str(idx)))
    acc_node = Node(NodeKind.ARR_ACC, elem.ntype, '', array, idx_node)
    return Node(NodeKind.OP_ASSIGN, elem.ntype, '=', acc_node, elem)


def array_declaration(name: str) -> Node:
    root = None
    elems = []

    while curr_token().kind != TokenKind.RBRACE:
        token = match_token_from(
            (TokenKind.INT_LIT, TokenKind.CHAR_LIT, TokenKind.IDENT))

        if curr_token().kind != TokenKind.RBRACE:
            match_token(TokenKind.COMMA)

        elems.append(token)

    arr = Def.arr_map[name]
    if len(elems) > arr.elem_cnt:
        print(
            f'array_declaration: Array {name} can only hold {arr.elem_cnt} elements')
        exit(1)

    elems.reverse()
    nodes = list(map(to_node, elems))

    idx = 0
    arr_node = Node(NodeKind.IDENT, type_of_ident(name), name)

    if len(nodes) == 1:
        return array_elem_declaration(arr_node, nodes.pop(), 0)

    while len(nodes) > 0:
        if root is None:
            node = nodes.pop()
            node2 = nodes.pop()
            root = Node(NodeKind.GLUE, void_type, '', array_elem_declaration(
                arr_node, node, idx), array_elem_declaration(arr_node, node2, idx + 1))
            idx += 2
        else:
            node = nodes.pop()
            root = Node(
                NodeKind.GLUE, void_type, '', root, array_elem_declaration(arr_node, node, idx))
            idx += 1

    return root


def declaration() -> Optional[Node]:
    name = match_token(TokenKind.IDENT).value
    match_token(TokenKind.COLON)

    var_type = type_of(curr_token().value)
    kind, meta_kind = var_type.kind, var_type.meta_kind
    next_token()

    elem_cnt = 0
    if not no_more_tokens() and curr_token().kind == TokenKind.LBRACE:
        next_token()

        meta_kind = VariableMetaKind.ARR
        elem_cnt = int(match_token(TokenKind.INT_LIT).value)
        match_token(TokenKind.RBRACE)

    if not no_more_tokens() and curr_token().kind == TokenKind.MULT:
        next_token()
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

        match_token(TokenKind.ASSIGN)

        node = token_list_to_tree()

        if not is_local:
            return None

        return Node(NodeKind.OP_ASSIGN, var_type, '=', Node(NodeKind.IDENT, var_type, full_name), node)

    if var_type.meta_kind == VariableMetaKind.STR:
        Def.str_map[full_name] = String(
            full_name, Def.var_off)

        match_token(TokenKind.ASSIGN)

        node = token_list_to_tree()
        return Node(NodeKind.OP_ASSIGN, var_type, '=', Node(NodeKind.IDENT, var_type, full_name), node)

    if var_type.meta_kind == VariableMetaKind.ARR:
        elem_type = VariableType(var_type.kind, VariableMetaKind.PRIM)
        Def.arr_map[full_name] = Array(
            full_name, elem_cnt, elem_type, Def.var_off)
        Def.var_off += size_of(elem_type) * elem_cnt

        if no_more_tokens():
            return None

        match_token(TokenKind.ASSIGN)
        match_token(TokenKind.LBRACE)

        return array_declaration(full_name)

    if var_type.meta_kind == VariableMetaKind.PTR:
        elem_type = VariableType(var_type.kind, VariableMetaKind.PTR)
        Def.ptr_map[full_name] = Pointer(full_name, elem_type, Def.var_off)

        match_token(TokenKind.ASSIGN)

        node = token_list_to_tree()
        return Node(NodeKind.OP_ASSIGN, var_type, '=', Node(NodeKind.IDENT, var_type, full_name), node)

    print(f'declaration: Unknown meta kind {meta_kind}')
    exit(1)
