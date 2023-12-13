# Mini Lang

A type-safe C successor that compiles directly to x86_64 assembly.

**Warning:** The language is still under development.
Some features are missing.

**Check out [acwj-git](https://github.com/DoctorWkt/acwj.git)**, DoctorWkt's tutorial is the main (best) source of inspiration of this project's structure.

## Features

* Minimal
* Compiled
* Typed
* Functional
* Inter-op with C functions

Minimal - As close as possible to actual assembly code while maintaining as many high-level features as possible.

## Links

* [Bug list](BUG.md)
* [TODO list](TODO.md)
* [License] (LICENSE.md)

## Syntax highlighter (VSCode)

Install the VSIX extension `./minilang-highlighter/minilang-highlighter-0.0.1.vsix`.

`Extensions -> Views and more actions... (top-left three dots) -> Install from VSIX...`

## QuickStart

**Warning:** Source files should be terminated by an extra `end` keyword due to reusing `Parser.compund_statement` to parse the program's logic.

`Main.py:44: root = Parser.compund_statement()`

### Primitives

```txt
void
int8
int16
int32
int64
```

### Literals

**Warning:** There is no safety measure regarding string literal manipulation. Doing this will most probably result in a segmentation fault.

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

**Warning:** Type definitions are not yet part of the language.

```txt
typedef int = int32
typedef ptr = void*
typedef str = int8*
typedef byte = int8
typedef char = int8
```

Compared to C, MiniLang's `void` type doesn't take up any space.
Thus, a stack variable of type void acts as a stack addr placeholder (its offset coincides with the next stack-allocated variable).

### Declaration/Assignment

```txt
# Declaration syntax
let variable: type = value
let pointer: type* = address
let array: type[n] = [elem1, elem2, ..., elemn]

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
