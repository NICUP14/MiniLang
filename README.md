# MiniLang

<img src="Logo.png" width="250px"></img>

> [!WARNING]
> The language is still under development.
Some features are missing.

A type-safe C successor that compiles directly to various platforms.

**Check out [acwj-git](https://github.com/DoctorWkt/acwj.git)**, DoctorWkt's tutorial is the main (best) source of inspiration of this project's structure.

## QuickStart

* [Language Documentation](QUICKSTART.md).
* [Standard Library Documentation](STDLIB.md).
* [Standard Library Usage Examples](docs/stdlib/examples.md).

## Design choices

* Modern
* Compiled
* Procedural
* Strongly typed
* Type and memory safe
* Closely match C features
* Bidirectionally compatible with C
* ML must be easy to learn and use
* ML abstractions introduce zero-overhead compared to C

## Motivation

The language is designed to closely **match c features** along with some **zero-overhead** quality of life improvements that you would find in a modern language, while maintaining the **ease of learning the language** (in about 10 minutes or less via [QUICKSTART](QUICKSTART.md)). Moreover, the type system is **stricter than c**, which prevents common bugs (flaws) of the c language. **Memory safety** is also a primary concern. As for c compatibility, the language is **bidirectionally compatible with c** (c can be used in ML, ML can be used in c).

## Goodies

* [RAII](QUICKSTART.md#raii)
* [Builtins](QUICKSTART.md#builtins)
* [Booleans](QUICKSTART.md#primitive-types)
* [References](QUICKSTART.md#reference-type)
* [Fixed-length integers](QUICKSTART.md#integer-primitives)
* [Fixed-length pointers](QUICKSTART.md#pointer-type)
* [Type inference](QUICKSTART.md#declarationassignment)
* [Heredocs](QUICKSTART.md#declarationassignment)
* [Aliases](QUICKSTART.md#aliases)
* [Defers](QUICKSTART.md#defer-statements)
* [Imports](QUICKSTART.md#import-statements)
* [Namespaces](QUICKSTART.md#namespace-statements)
* [Hygienic macros](QUICKSTART.md#macros)
* [For-each loops](QUICKSTART.md#for-loops)
* Generic functions
* [Function overloading](QUICKSTART.md#function-overloading)
* [Function signatures](QUICKSTART.md#signatures-function-pointers)
* [Uniform function call syntax (UFCS)](QUICKSTART.md#uniform-function-call-syntax-ufcs)
* [Multi-line statements](QUICKSTART.md#multi-line-statements)

## Branches

* [main](https://github.com/NICUP14/MiniLang/tree/main)
* [unstable](https://github.com/NICUP14/MiniLang/tree/unstable)

> [!WARNING]
> The **unstable** branch is updated more often than the **main** (stable) branch and offers access to experimental features, but is more prone to breakage/bugs.

## Links

* [Ideas](IDEAS.md)
* [Bug list](BUG.md)
* [TODO list](TODO.md)
* [License](LICENSE)
* [QuickStart](QUICKSTART.md)
* [STDLIB](STDLIB.md)

To suggest features/fixes, modify `IDEAS.md`/`BUG.md` and submit a pull request or contact me via the email address in my github profile.

## Syntax highlighter (VSCode)

Install the VSIX extension `./minilang-highlighter/minilang-highlighter-0.0.1.vsix`.

`Extensions -> Views and more actions... (top-left three dots) -> Install from VSIX...`

## Manage ML projects

### Running samples and tests

To run a sample or test, specify its directory using the `-C` option in `mlpx` with arguments `build and run`.

```txt
python mlpx -C tests/test build and run
```

### Creating projects

> [!IMPORTANT]
> It's recommended to use the `mlpx` build tool as it's specifically designed for this purpose: no libary redundancy and no configuration compared to using the `make` build tool.

Creating a `MiniLang` project is easy and straight-forward using the `mlpx` utility, which provides two ways with differing build tools.

```txt
# Using the mlpx build tool
python mlpx init my_new_project

# Using the make build tool
python mlpx makefile-init my_new_project
```

### Build tools

* [Makefile](docs/build-tool/makefile.md)
* [MLPX](docs/build-tool/mlpx.md)

## Code statistics

```txt
----------------------------------------------------------------------------------------        
File                                      blank        comment           code
----------------------------------------------------------------------------------------        
src\Parser.py                               482             92           1846
src\Def.py                                  320             74           1108
src\Gen.py                                  217            134            697
src\Lexer.py                                 43              1            351
src\backend\c\CWalker.py                     25             17            203
src\backend\ml\MLWalker.py                   18              6            179
src\backend\c\CDef.py                        50              1            155
src\GenStr.py                                16              1            129
src\Snippet.py                               38              0            106
src\Main.py                                  14              2             79
src\backend\ml\MLDef.py                      14              2             56
src\backend\Walker.py                        16              3             53
----------------------------------------------------------------------------------------        
SUM:                                       1253            333           4962
----------------------------------------------------------------------------------------
```

> [!NOTE]
> Statistics were generated with [cloc](https://github.com/AlDanial/cloc.git).
<!-- 
> Current statistics are up-to-date.
-->

## Usage

> [!WARNING]
> The asm compiler backend is currently far outdated. The latest features exclusively require the c and ml compiler backends.

```txt
Usage: Main.py [options]

The mini language compiler, Version: 1.0.0, Source:
https://github.com/NICUP14/MiniLang.git

Options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output=OUTPUT
                        Write contents to OUTPUT; When set, no-color is        
                        enabled by default.
  -d, --debug           Dry run; Print the human-friendly AST representation.  
                        Overrides any specified backend option.
  -c, --no-color        Do not use ANSI color sequences in the output.
  -C, --no-comment      Do not include human-readable comments in the
                        generated assembly.
  -I INCLUDE, --include=INCLUDE
                        Add the directory to the include path.
  -b BACKEND, --backend=BACKEND
                        Specify which compiler backend to use. Choose between  
                        c, asm and ml.
```

## Samples

* [HelloWorld](https://github.com/NICUP14/MiniLang/tree/main/samples/helloworld)
* [Max](https://github.com/NICUP14/MiniLang/tree/main/samples/max)
* [Fib](https://github.com/NICUP14/MiniLang/tree/main/samples/fib)
* [IO](https://github.com/NICUP14/MiniLang/tree/main/samples/io)
* [Calc](https://github.com/NICUP14/MiniLang/tree/main/samples/calc)
* [FizzBuzz](https://github.com/NICUP14/MiniLang/tree/main/samples/fizzbuzz)
* [Str-ufcs](https://github.com/NICUP14/MiniLang/tree/main/samples/str-ufcs)
* [Task-mgr](https://github.com/NICUP14/MiniLang/tree/main/samples/task-mgr)
* [Printf](https://github.com/NICUP14/MiniLang/tree/main/samples/printf)
* [Fractal](https://github.com/NICUP14/MiniLang/tree/main/samples/fractal)

> [!NOTE]
> All MiniLang samples (example projects) are located within the `samples` directory. All samples are written entirely in ML.

### Hello World

```txt
# From samples/helloworld/src/main.ml:
import stdlib.io.print

fun main: int32
    print "Hello World!"
    ret 0
end
```

### String (UFCS)

```txt
# From samples/str-ufcs/src/main.ml:
import stdlib.io.print
import stdlib.string

fun main: int32
    # Is equivalent to:
    # print(concat(str("Hello "), str("World!")))
    (str("Hello ").
        concat(str("World!")).
        print)
end
```

### FizzBuzz

```txt
# From samples/fizzbuzz/src/main.ml:
import stdlib.io.print

fun fizz_buzz(num: int64): void
    let idx = 1

    while idx <= num
        if idx % 15 == 0
            println(idx, ": FizzBuzz")
        elif idx % 3 == 0
            println(idx, ": Fizzz")
        elif idx % 5 == 0
            println(idx, ": Buzz")
        end

        idx = idx + 1
    end
end

fun main(): int64
    fizz_buzz(15)
    ret 0
end
```

## License

Copyright © 2023-2024 Nicolae Petri

Licensed under the MIT License.
