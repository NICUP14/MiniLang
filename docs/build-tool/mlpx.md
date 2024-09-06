# MiniLang Project Extension

A convenient tool for managing `MiniLang` projects.

## Project skeleton structure

```txt
skel/
└── src
    └── main.ml
```

## Examples

### Cleaning

```txt
# Cleaning a project
$ python mlpx -C tests/test/ clean
Cleaning tests/test/bin
rm -vrf tests/test/bin
removed 'tests/test/bin/main.c'
removed 'tests/test/bin/main.exe'
removed directory 'tests/test/bin'
Done!
```

### Running a project

```txt
$ python mlpx -C tests/test/ run
> Running tests/test/bin/main
tests/test/bin/main
<Output hidden>
> Done!
```

### Building a project

```txt
$ python mlpx -C tests/test/ build
> Running default option on tests/test/
python3 ./src/Main.py -C -I ./include -o tests/test/bin/main.c tests/test/src/main.ml
gcc -g -O2 ./skel/include/*.c -I ./skel/include tests/test/bin/main.c -o tests/test/bin/main
> Done!
```

### Building a project using a custom build option

```txt
$ python mlpx -C tests/test/ build cdebug
> Running cdebug option on tests/test/
<Output hidden>
> Done!
```

### Building and running a project

```txt
$ python mlpx -C tests/test/ build and run
> Running default option on tests/test/
python3 ./src/Main.py -C -I ./include -o tests/test/bin/main.c tests/test/src/main.ml
gcc -g -O2 ./skel/include/*.c -I ./skel/include tests/test/bin/main.c -o tests/test/bin/main
> Running tests/test/bin/main
tests/test/bin/main
<Output hidden>
> Done!
```

## Commands

> [!TIP]
> Commands can be chained using the `and` separator: `python mlpx build and run`.

Command          | Action
-----------------|-----------
`run`            | Runs the executable created by the `build` command.
`build  [opts]`  | Builds the current project using build options `opts`.
`rclean [dirs]`  | Recursively cleans all projects in `dirs`.
`clean  [dirs]`  | Cleans the projects specified by `dirs`.
`init   [proj]`  | Initializes a new `MiniLang` project named `proj`. (coming soon)

## Options

Shorthand | Option      | Default        | Description
----------|-------------|----------------|------------
-h        | --help      | -              | Show this help message and exit.
-C        | --proj-path | `./`           | Specify the project path.
-p        | --path      | `./`           | Specify the MiniLang project path.
-b        | --build-dir | `bin`          | Specify the build directory.
-o        | --build-opt | `default`      | Specify the build option.
-n        | --name      | `main`         | Specify the project's name.
-i        | --include   | `include`      | Speficy the MiniLang compiler include path.
-I        | --c-include | `skel/include` | Specify the C compiler include path.
-q        | --quiet     | -              | Run in quiet mode; Does not show compile commands.  Overrides "-m".
-m        | --no-msg    | -              | Run in script mode; Does not show mlpx logs.
-c        | --no-color  | -              | Run in text mode; Does not use colors.

## Build options

Option   | Shorthand | Description
---------|-----------|------------
`clean`  | -         | Removes the build directory.
`deault` | `def`     | Compiles the project and creates an executable.
`debug`  | `dbg`     | Compiles using the `MiniLang` backend and prints to `stdout`.
`cdebug` | `cdbg`    | Compiles using the `C` backend and prints to `stdout`.
