import Def
import Gen
import Parser
import os
import sys
import optparse
from os.path import exists
from Def import Node
from Def import Color
from Def import color_str
from Def import print_error
from Def import glue_statements
from backend.c.CWalker import c_walk
from backend.ml.MLWalker import ml_walk

ml_file_type = 'ml'
default_in_file = f'main.{ml_file_type}'


def ml_preamble(module: str) -> Node:
    module_source = f'{module}.ml'
    for module_dir in Def.include_list:
        other_source = os.path.join(module_dir, module_source)
        print('DBG:', other_source, exists(other_source))
        if exists(other_source):
            module_source = other_source
            break

    if not exists(module_source):
        print_error('ml_preamble',
                    f'Module \'{module_source}\' does not exist.')

    Def.included.add(module_source)
    return Parser.Parser().parse(module_source)


if __name__ == '__main__':
    desc = ', '.join(['The mini language compiler',
                      'Version: 1.0.0',
                      'Source: https://github.com/NICUP14/MiniLang.git'])

    parser = optparse.OptionParser(description=desc)
    # parser.add_option('-i', '--input', default=default_in_file,
    #                   help='Read contents from INPUT.')
    parser.add_option('-o', '--output', default='stdout',
                      help='Write contents to OUTPUT; When set, no-color is enabled by default.')
    parser.add_option('-d', '--debug', action='store_true',
                      help='Dry run; Print the human-friendly AST representation. Overrides any specified backend option.')
    parser.add_option('-c', '--no-color', action='store_true',
                      help='Do not use ANSI color sequences in the output.')
    parser.add_option('-C', '--no-comment', action='store_true',
                      help='Do not include human-readable comments in the generated assembly.')
    parser.add_option('-I', '--include', action='append',
                      help='Add the directory to the include path.')
    parser.add_option('-b', '--backend', default='c',
                      help='Specify which compiler backend to use. Choose between c, asm and ml.')
    values, in_files = parser.parse_args()
    values_dict = vars(values)

    if len(in_files) == 0:
        in_files = [default_in_file]
    out_file = values_dict.get('output')
    backend = values_dict.get('backend')

    include_list = values_dict.get('include')
    Def.include_list = include_list if include_list else []
    Def.color_enabled = not values_dict.get('no_color')
    Def.comments_enabled = not values_dict.get('no_comment')

    if out_file != 'stdout':
        Def.color_enabled = False
        Def.stdout = open(values_dict.get('output'), 'w')

    for in_file in in_files:
        if not exists(in_file):
            print(
                f'{sys.argv[0]}: {color_str(Color.FAIL, f"{in_file} does not exist.")}')
            exit(1)

    for in_file in in_files:
        parser = Parser.Parser()
        preamble = ml_preamble(os.path.join('stdlib', 'builtin'))
        root = glue_statements([preamble, parser.parse(in_file)])

        if values_dict.get('debug'):
            Def.print_stdout(ml_walk(root))
        else:
            if backend == 'c':
                Def.print_stdout(c_walk(root))
            elif backend == 'ml':
                Def.print_stdout(ml_walk(root))
            elif backend == 'asm':
                Gen.gen(root)
            else:
                print(
                    f'{sys.argv[0]}: {color_str(Color.FAIL, f"Unknown backend {backend}.")}')
