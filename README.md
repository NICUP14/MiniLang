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
src\Gen.py                         177             41            601
src\Def.py                         158             45            525
src\Parser.py                      131             11            506
src\Lexer.py                        40              1            231
src\Snippet.py                      38              0            106
src\GenStr.py                       15              1            103
src\Main.py                          9              0             45
-------------------------------------------------------------------------------
SUM:                               568             99           2117
-------------------------------------------------------------------------------
```

> [!NOTE]
> Current statistics are out-of-date.
> Statistics were generated with [cloc](https://github.com/AlDanial/cloc.git).

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

## QuickStart

> [!WARNING]
> Source files should be terminated by an extra `end` keyword due to reusing `Parser.compund_statement` to parse the program's logic.

`Parser.py:98: return self.compund_statement()`

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
> There is no safety measure regarding string literal manipulation. Doing this will most probably result in a segmentation fault.

```txt
# String literal (int8*)
"abc"

# Character literal (int8)
'c'

# Undefined behaviour
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

Compared to C, MiniLang's `void` type doesn't take up any space.
Thus, a stack variable of type void acts as a stack addr placeholder (its offset coincides with the next stack-allocated variable).

### Declaration/Assignment

```txt
# Declaration syntax
# Recommended naming convention: snake_case
# The type for non-array variables is optional (type inference)
let variable: type = value
let pointer: type* = address
let inferred = &variable
let array: type[n] = [elem1, elem2, ..., elemn]

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

### Functions

```txt
# External function syntax (Useful for C inter-op)
extern fun exit(status: int32): void
extern fun printf(msg: int8*, ...): int32

# Function syntax
# fun myfun(param1: type, param2: type2, ...)
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
