# QuickStart

> [!WARNING]
> Source files should be terminated by an extra `end` keyword due to reusing `Parser.compund_statement` to parse the program's logic.

## Primitive Types

Meta type | Arithmetic | Implicit cast-to-pointer
----------|------------|-------------------------
Integer   | Yes        | No
Boolean   | No         | No
Pointer   | No         | Yes
Reference | No         | No*
Array     | No         | Yes

### Boolean primitives

* `bool`

### Integer primitives

* `void`
* `int8`
* `int16`
* `int32`
* `int64`

### Array type

Array: `type[n]`

> [!TIP]
> For array types, the `len_of` builtin returns the element capacity of the array, while the `size_of` builtin returns the size capacity.

### Pointer type

Normal Pointer: `type*`

Fixed-length pointer: `type[n]*`

> [!TIP]
> The advantage of using fixed-length pointers over normal pointers is that it enables the use of `len_of` and `size_of` similar to array types.

### Reference type

Reference: `type&`

```txt
fun swap(term1: int64&, term2: int64&): void
    let tmp: int64 = term1
    term1 = term2
    term2 = tmp
end

fun main(): int64
    let term1 = 15
    let term2 = 30
    swap(&term1, &term2)
    printf("Terms: %lld %lld", term1, term2)
    ret 0
end
end
```

> [!IMPORTANT]
> Pointers are often used for tasks involving dynamic memory allocation and low-level operations, while references are commonly used for more straightforward and safer variable access, especially for passing variables to functions.

## Literals

> [!WARNING]
> There is no safety measure regarding string literal manipulation. Doing this results in undefined behavior.

```txt
# Integer literal (int64)
0

# Boolean literal (bool)
true
false

# String literal (int8*)
"abc"

# Character literal (int8)
'c'

# Undefined behavior
"abc" at 0 = 'd'
```

## Builtins

Builtin            | Return type          | Returns
-------------------|----------------------|----------
fun                | String literal       | Function name
file               | String literal       | Source file
line               | String literal       | Source line
lineno             | Integer literal      | Source line number
ma_cnt             | Integer literal      | Macro argument expression count*
off_of(ident)      | Integer literal      | Variable stack offset
len_of(ident)      | Integer literal      | Element count of the array
size_of(ident)     | Integer literal      | Variable size
type_of(expr)      | String literal       | Expression type
cast("type", expr) | Any                  | The expression cast to type
asm("statement")   | Void                 | -

```txt
# Source code (before parsing)
# From tests/builtins/main.ml:
fun main(): int64
    let a: int8* = 0
    printf("off_of(a): %lld", off_of(a))
    printf("size_of(a): %lld", size_of(a))
    printf("%s:%s: Test", file, fun)
    assert_extra(a != 0, line, file, lineno)
    ret 0
end

# AST representation (after parsing)
# Command: "python src/Main.py -i tests/builtins/main.ml -d"
fun main()
  ((int8*)(main_a) = 0)
  printf("off_of(a): %lld\n", 16)
  printf("size_of(a): %lld\n", 8)
  printf("%s:%s: Test\n", "main.ml", "main")
  assert_extra(((int8*)(main_a) != 0), "assert_extra(a != 0, line, file, lineno)", "main.ml", 9)
  ret 0
end
```

## Operators

Symbol | Type   | Location | Operation
-------|--------|----------|----------
\+     | Binary | -        | Plus
\-     | Binary | -        | Minus
\*     | Binary | -        | Multiply
/      | Binary | -        | Divide
%      | Binary | -        | Modulo
\|     | Binary | -        | Bitwise or
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

## Inline assembly

> [!WARNING]
> The `asm` builtin does not validate any inline assembly code passed as a parameter (by design). Thus, manually shrinking or growing the function stack  leads to undefined behavior.

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

## Type definitions

> [!Note]
> The type definitions defined below are part of the standard library. (`stdlib/stddef.ml`)

```txt
typedef int = int64
typedef ptr = void*
typedef cint = int32
typedef cstr = int8*
typedef byte = int8
typedef char = int8
typedef size_t = int64
```

## Declaration/Assignment

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

## If statements

```txt
# If statement syntax
# if expression1 sign expression2
if a + 5 > 20
    a = 20
else
    a = 10
end
```

## While loops

```txt
# While loop syntax
# while expression sign expression2
while a >= 10
    a = a / 10
end
```

## Import statements

```txt
# Import statement syntax
# Note: This instructs the compiler to include the cstdlib module (cstdlib.ml) in the build.
import "../../cstdlib"
```

## Defer statements

> [!TIP]
> The `defer` statement is particularly useful for resource clean-up, such as freeing allocated memory, closing files or running cleanup tasks at the end of the function scope.

```txt
# Source code (before parsing)
# From tests/defer/main.ml:
fun main(): int64
    let arr: int64[5] = [0, 1, 2, 4, 4]
    let arr_size = size_of "arr"

    let ptr: int64* = malloc(arr_size)
    memcpy(ptr, arr, arr_size)
    defer free(ptr)

    let idx = 0
    while idx < len_of("arr")
        printf("%d", arr at idx)
        idx = idx + 1
    end
    ret 0
end

# AST representation (after parsing)
# Command: "python src/Main.py -i tests/defer/main.ml -d"
fun main()
  ((int64[5])(main_arr)[0] = 0)
  ((int64[5])(main_arr)[1] = 1)
  ((int64[5])(main_arr)[2] = 2)
  ((int64[5])(main_arr)[3] = 4)
  ((int64[5])(main_arr)[4] = 4)
  ((int64)(main_arr_size) = 40)

  ((int64*)(main_ptr) = malloc((int64)(main_arr_size)))
  memcpy((int64*)(main_ptr), (int64[5])(main_arr), (int64)(main_arr_size))

  ((int64)(main_idx) = 0)
  while ((int64)(main_idx) < 5)
    printf("%d", (int64[5])(main_arr)[(int64)(main_idx)])
    ((int64)(main_idx) = ((int64)(main_idx) + 1))
  end

  free((int64*)(main_ptr))
  ret 0
end
```

## Macros

Compared to C/C++ macros, the ML macro system is hygienic. That means that each macro is represented internally by an AST (pre-processor-less macros). On each macro call, the parser substitutes each macro argument with their invoked counterpart.

```txt
# Macro syntax
# macro mymacro
# macro mymacro(arg1, arg2, arg3, ...)

# From stdlib/stddef.ml:
macro int(_expr)
    cast("int", _expr)
end

# The supports C++-like type casts trough macros
let myint = int(50)
```

> [!Note]
> Macros are variadic by default, Thus, the last argument of a macro accepts a variable number of expressions and stores the expression count in `ma_cnt`. This feature is particularly useful for passing the parameter count to a variadic function.

```txt
# From samples/max/main.ml
fun _max(cnt: int64, ...): int64
    let vlist: int64[3]
    asm "stack_snapshot"
    va_start(&vlist)
    va_arg(&vlist)

    let arg = 0
    let max = 0
    for_until(0, cnt, expr(arg = va_arg(&vlist)), expr(max = cond(arg > max, arg, max)))

    ret max
end

macro max(args)
    _max(ma_cnt, args)
end
```

## Functions

> [!TIP]
> For single-parameter and no-parameter functions the use of parenthesis is optional.
> `no_param` or `no_param()`
> `single_param param` or `single_param(param)`

```txt
# External function syntax (Useful for C inter-op)
extern fun exit(status: int32): void
extern fun printf(msg: int8*, ...): int32

# Function syntax
# fun myfun: ret_type
# fun myfun(param_1: type, param_2: type2, ...): ret_type
fun U64ToStrLen(nr: int64): int64
    let cnt: int64 = 0
    while nr != 0
        nr = nr / 10
        cnt = cnt + 1
    end

    ret cnt
end
```
