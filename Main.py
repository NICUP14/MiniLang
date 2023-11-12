import Lexer
import Parser
import Def
import Gen
import GenStr


if __name__ == '__main__':
    input_file = 'test.ml'
    Parser.parser_lines = list(filter(
        lambda l: l.lstrip('\t ') != '\n' and not l.lstrip('\t ').startswith('#'), open(input_file, 'r').readlines()))

    # print(Parser.parser_lines)

    Parser.parser_tokens = Parser.tokenize(Parser.curr_line())
    # while not Parser.no_more_lines():
    #     root = Parser.statement()
    #     Gen.gen(root)

    root = Parser.compund_statement()
    # print(root)
    # print()
    # print(GenStr.tree_str(root))
    # print()
    Gen.gen(root)
