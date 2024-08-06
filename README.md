# Mini Lang

<img src="Logo.png" width="250px"></img>

A type-safe C successor that compiles directly to x86_64 assembly.

> [!WARNING]
> The language is still under development.
Some features are missing.

**Check out [acwj-git](https://github.com/DoctorWkt/acwj.git)**, DoctorWkt's tutorial is the main (best) source of inspiration of this project's structure.

## Branches

* [main](https://github.com/NICUP14/MiniLang/tree/main)
* [unstable](https://github.com/NICUP14/MiniLang/tree/unstable)

> [!WARNING]
> The **unstable** branch is updated more often than the **main** (stable) branch and offers access to experimental features, but is more prone to breakage/bugs.

## Features

* Minimal
* Compiled
* Typed
* Functional
* Hygienic macro system
* C function interoperability

Minimal - As close as possible to actual assembly code while maintaining as many high-level features as possible.

## Links

> [!IMPORTANT]
> The language documentation is provided at [QuickStart](QUICKSTART.md).

* [Ideas](IDEAS.md)
* [Bug list](BUG.md)
* [TODO list](TODO.md)
* [License](LICENSE)
* [QuickStart](QUICKSTART.md)

To suggest features/fixes, modify `IDEAS.md`/`BUG.md` and submit a pull request or contact me via the email address in my github profile.

## Syntax highlighter (VSCode)

Install the VSIX extension `./minilang-highlighter/minilang-highlighter-0.0.1.vsix`.

`Extensions -> Views and more actions... (top-left three dots) -> Install from VSIX...`

## Code statistics

```txt
-------------------------------------------------------------------------------
File                             blank        comment           code
-------------------------------------------------------------------------------
src/Parser.py                      251             46            981
src/Def.py                         210             56            738
src/Gen.py                         189             66            649
src/Lexer.py                        43              0            296
src/GenStr.py                       17              1            130
src/Snippet.py                      38              0            106
src/Main.py                          9              0             45
-------------------------------------------------------------------------------
SUM:                               757            169           2945
-------------------------------------------------------------------------------
```

> [!NOTE]
> Statistics were generated with [cloc](https://github.com/AlDanial/cloc.git).
<!-- 
> Current statistics are out-of-date.
-->

## Usage

```txt
Usage: Main.py [options]

The mini language compiler, Version: 1.0.0, Source:
https://github.com/NICUP14/MiniLang.git

Options:
  -h, --help            show this help message and exit
  -i INPUT, --input=INPUT
                        Read contents from INPUT.
  -o OUTPUT, --output=OUTPUT
                        Write contents to OUTPUT; When set, no-color is
                        enabled by default.
  -d, --debug           Dry run; Print the human-friendly AST representation.
  -c, --no-color        Do not use ANSI color sequences in the output.
  -C, --no-comment      Do not include human-readable comments in the
                        generated assembly.
```

## Samples

* [HelloWorld](https://github.com/NICUP14/MiniLang/tree/main/samples/helloworld)
* [Max](https://github.com/NICUP14/MiniLang/tree/main/samples/max)
* [Fib](https://github.com/NICUP14/MiniLang/tree/main/samples/fib)
* [FizzBuzz](https://github.com/NICUP14/MiniLang/tree/main/samples/fizzbuzz)
* [Printf](https://github.com/NICUP14/MiniLang/tree/main/samples/printf)

> [!NOTE]
> All MiniLang samples (example projects) are located within the `samples` directory. All samples are written entirely in ML.

> [!NOTE]
> The `printf` sample is currently broken due to a type system update.

## Hello World

```txt
# From samples/helloworld.ml:
import "../../stdlib/c/cstdlib"

fun main: int64
    puts "Hello World!"
    ret 0
end
end
```

## License

Copyright © 2023 Nicolae Petri

Licensed under the MIT License.
