import Parser
import Gen
import GenStr
import optparse
import sys
import Def
from Def import Color
from Def import color_str
from os.path import exists

default_in_file = 'main.ml'
default_out_file = 'main.asm'

if __name__ == '__main__':
    desc = ', '.join(['The mini language compiler',
                      'Version: 1.0.0',
                      'Source: https://github.com/NICUP14/MiniLang.git'])

    parser = optparse.OptionParser(description=desc)
    parser.add_option('-i', '--input', default=default_in_file,
                      help='read contents from INPUT')
    parser.add_option('-o', '--output', default=default_out_file,
                      help='write contents to OUTPUT')
    parser.add_option('-d', '--debug', action='store_true',
                      help='Dry run; Print the human-friendly AST representation')
    parser.add_option('-c', '--no-color', action='store_true',
                      help='Do not use ANSI color sequences in the output.')
    values, _ = parser.parse_args()
    values_dict = vars(values)

    in_file = values_dict.get('input')
    out_file = values_dict.get('output')

    if not exists(in_file):
        print(
            f'{sys.argv[0]}: {color_str(Color.FAIL, f"{in_file} does not exist.")}')
        exit(1)

    Parser.parser_lines = list(filter(
        lambda l: l.lstrip('\t ') != '\n' and not l.lstrip('\t ').startswith('#'), open(in_file, 'r').readlines()))
    Parser.parser_tokens = Parser.tokenize(Parser.curr_line())
    root = Parser.compund_statement()

    Def.color_enabled = not values_dict.get('no_color')
    if values_dict.get('debug'):
        print(GenStr.tree_str(root))
    else:
        Gen.gen(root)
