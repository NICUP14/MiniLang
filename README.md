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
* Strongly typed
* Function overloading
* Hygienic macro system
* C function interoperability
* Uniform function call syntax (UFCS)

Minimal - As close as possible to actual assembly code while maintaining as many high-level features as possible.

## Links

> [!IMPORTANT]
> The language documentation is provided at [QuickStart](QUICKSTART.md).

> [!IMPORTANT]
> The standard library documentation is coming soon...

* [Ideas](IDEAS.md)
* [Bug list](BUG.md)
* [TODO list](TODO.md)
* [License](LICENSE)
* [QuickStart](QUICKSTART.md)

To suggest features/fixes, modify `IDEAS.md`/`BUG.md` and submit a pull request or contact me via the email address in my github profile.

## Syntax highlighter (VSCode)

Install the VSIX extension `./minilang-highlighter/minilang-highlighter-0.0.1.vsix`.

`Extensions -> Views and more actions... (top-left three dots) -> Install from VSIX...`

## Create a ML project

> [!IMPORTANT]
> The ML project creator utility (`ml-init`) will be available soon...

> [!WARNING]
> For new ML projects, makefile parameters `ML`, `MLLIB` need to be adjusted if they are specified by a relative path. Check **Makefile** section below.

```txt
# I. Copy project skeleton
cp -r skel <PATH_TO_PROJ>

# II. Configure makefile parameters (ML, MLLIB)
$EDITOR <PATH_TO_PROJ>/Makefile
```

### Project skeleton structure

```txt
skel/
├── include
│   ├── gc.c
│   ├── gc.h
│   ├── gc-LICENSE
│   ├── log.c
│   ├── log.h
│   ├── sds.c
│   ├── sds.h
│   ├── sdsalloc.h
│   └── sds-LICENSE
├── Makefile
└── src
    ├── gc.ml
    └── main.ml
```

The [sds](https://github.com/antirez/sds) (Simple Dynamic Strings) library is required by the ML string library. (`stdlib/string.ml`)

The [gc](https://github.com/mkirchner/gc) library will be required by the ML alloc library. (*Coming soon*)

### Makefile

#### Recipes

Recipe   | Alias  | Backend
---------|--------|--------
default  | def, c | c
cdebug   | cdbg   | c
debug    | dbg    | ml
assemble | asm    | asm

### Parameters

Parameter | Description
----------|------------------------------
CC        | Path to c compiler
ML        | Path to ML compiler
MLLIB     | Path to ML standard library
CFLAGS    | Options passed to c compiler
MLFLAGS   | Options passed to ML compiler

## Code statistics

```txt
----------------------------------------------------------------------------------------
File                                      blank        comment           code  
----------------------------------------------------------------------------------------
src\Parser.py                               303             46           1249  
src\Def.py                                  262             65            901  
src\Gen.py                                  217            134            697  
src\Lexer.py                                 43              0            322
src\backend\c\CWalker.py                     18              8            173
src\backend\c\CDef.py                        45              1            140
src\GenStr.py                                16              1            129
src\Snippet.py                               38              0            106
src\backend\ml\MLWalker.py                   10              0            106
src\Main.py                                   9              2             64
src\backend\Walker.py                        15              1             50
----------------------------------------------------------------------------------------
SUM:                                        976            258           3937
----------------------------------------------------------------------------------------
```

> [!NOTE]
> Statistics were generated with [cloc](https://github.com/AlDanial/cloc.git).
<!-- 
> Current statistics are up-to-date.
-->

## Usage

> [!WARNING]
> The ML and asm compiler backends are currently far outdated. The latest features exclusively require the c compiler backend.

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
* [FizzBuzz](https://github.com/NICUP14/MiniLang/tree/main/samples/fizzbuzz)
* [Printf](https://github.com/NICUP14/MiniLang/tree/main/samples/printf)

> [!NOTE]
> All MiniLang samples (example projects) are located within the `samples` directory. All samples are written entirely in ML.

## Hello World

```txt
# From samples/helloworld.ml:
import "stdlib/print"

fun main: int32
    print "Hello World!"
    ret 0
end
end
```

## License

Copyright © 2023 Nicolae Petri

Licensed under the MIT License.
