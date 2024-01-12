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
* Inter-op with C functions

Minimal - As close as possible to actual assembly code while maintaining as many high-level features as possible.

## Links

* [Ideas](IDEAS.md)
* [Bug list](BUG.md)
* [TODO list](TODO.md)
* [License](LICENSE)

To suggest features/fixes, modify `IDEAS.md`/`BUG.md` and submit a pull request or contact me via the email address in my github profile.

## Syntax highlighter (VSCode)

Install the VSIX extension `./minilang-highlighter/minilang-highlighter-0.0.1.vsix`.

`Extensions -> Views and more actions... (top-left three dots) -> Install from VSIX...`

## Code statistics

```txt
-------------------------------------------------------------------------------
File                             blank        comment           code
-------------------------------------------------------------------------------
src/Gen.py                         176             43            600
src/Def.py                         158             45            525
src/Parser.py                      133             11            521
src/Lexer.py                        40              1            235
src/Snippet.py                      38              0            106
src/GenStr.py                       15              1            105
src/Main.py                          9              0             45
-------------------------------------------------------------------------------
SUM:                               569            101           2137
-------------------------------------------------------------------------------
```

<!--
> [!NOTE]
> Current statistics are out-of-date.
> Statistics were generated with [cloc](https://github.com/AlDanial/cloc.git).
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

* [Fib](https://github.com/NICUP14/MiniLang/tree/unstable/samples/fib)
* [FizzBuzz](https://github.com/NICUP14/MiniLang/tree/unstable/samples/fizzbuzz)
* [Printf](https://github.com/NICUP14/MiniLang/tree/main/samples/printf)

> [!NOTE]
> All MiniLang samples (example projects) are located within the `samples` directory. All samples are written entirely in ML.

## QuickStart

> [!WARNING]
> Source files should be terminated by an extra `end` keyword due to reusing `Parser.compund_statement` to parse the program's logic.

### Primitives

```txt
void
int8
int16
int32
int64
```

### Literals

> [!WARNING]
> There is no safety measure regarding string literal manipulation. Doing this results in undefined behavior.

```txt
# String literal (int8*)
"abc"

# Character literal (int8)
'c'

# Undefined behavior
"abc" at 0 = 'd'

```

### Operators

Symbol | Type   | Location | Operation
-------|--------|----------|----------
\+     | Binary | -        | Plus
\-     | Binary | -        | Minus
\*     | Binary | -        | Multiply
/      | Binary | -        | Divide
%      | Binary | -        | Modulo
|      | Binary | -        | Bitwise or
&      | Binary | -        | Bitwise and
=      | Binary | -        | Assignment
at     | Binary | -        | Array access
==     | Binary | -        | Comparison (Equals)
!=     | Binary | -        | Negated comparison (Not equals)
<=     | Binary | -        | Less-than-or-equal comparison
\>=    | Binary | -        | Greater-than-or-equal comparison
<      | Binary | -        | Less-than comparison
\>     | Binary | -        | Greater-than comparison
&      | Unary  | Prefix   | Address
\*     | Unary  | Prefix   | Dereference

### Inline assembly

> [!WARNING]
> The `asm` built-in does not validate any inline assembly code passed as a parameter (by design). Thus, manually shrinking or growing the function stack  leads to undefined behavior.

```txt
# From samples/printf/va_utils.ml:
asm ".macro stack_snapshot"
asm "   push %r9"
asm "   push %r8"
asm "   push %rcx"
asm "   push %rdx"
asm "   push %rsi"
asm "   push %rdi"
asm ".endm"
...

# From samples/printf/printf.ml:
fun custom_printf(format: int8*, ...): void
    let va_list: int64[3]

    asm "stack_snapshot"
    va_start(va_list)
    va_arg(va_list)
    asm "stack_rewind"
...

# Undefined behavior
asm "sub $48, %rsp"

```

### Type definitions

> [!WARNING]
> The type definitions defined below are not yet part of the language.

```txt
typedef int = int32
typedef ptr = void*
typedef cstr = int8*
typedef byte = int8
typedef char = int8
```

### Declaration/Assignment

```txt
# Declaration syntax
# Recommended naming convention: snake_case
# The type for non-array variables is optional (type inference)
let variable: type = value
let pointer: type* = address
let inferred = &variable
let array: type[n] = [elem_1, elem_2, ..., elem_n]

# String & heredocs declaration syntax
let str: cstr = "abcd"
let heredoc_str: cstr = <<-
    \end
    HELLO end
    HELLO WORLD
    HELLO FROM BELOW
end

# Array accesses (2 equivalent methods)
array at i = 15
array[i] = 15
```

### If statements

```txt
# If statement syntax
# if expression1 sign expression2
if a + 5 > 20
    a = 20
else
    a = 10
end
```

### While loops

```txt
# While loop syntax
# while expression sign expression2
while a >= 10
    a = a / 10
end
```

### Import statements

```txt
# Import statement syntax
# Note: This instructs the compiler to include the cstdlib module (cstdlib.ml) in the build.
import cstdlib
```

### Functions

```txt
# External function syntax (Useful for C inter-op)
extern fun exit(status: int32): void
extern fun printf(msg: int8*, ...): int32

# Function syntax
# fun myfun(param_1: type, param_2: type2, ...)
fun U64ToStrLen(nr: int64): int64
    let cnt: int64 = 0
    while nr != 0
        nr = nr / 10
        cnt = cnt + 1
    end

    ret cnt
end
```

## License

Copyright © 2023 Nicolae Petri

Licensed under the MIT License.
