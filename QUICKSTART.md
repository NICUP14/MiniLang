# QuickStart

## Primitive Types

Meta type | Arithmetic | Implicit cast-to-pointer
----------|------------|-------------------------
Integer   | Yes        | No
Float     | Yes        | No
Boolean   | No         | No
Pointer   | No         | Yes
Reference | No         | No*
Array     | No         | Yes

### Void primitive

* `void`

### Boolean primitive

* `bool`

### Integer primitives

* `int8`
* `int16`
* `int32`
* `int64`

### Float primitives

* `float32`
* `float64`

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

Pointers are often used for tasks involving dynamic memory allocation and low-level operations, while references are commonly used for more straightforward and safer variable access, especially for passing variables to functions.

## Literals

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
```

## Builtins

> [!TIP]
> The `type_of` builtin can be used in combination with the `cast` builtin to cast a value using the inferred type of an expression:  `cast(type_of(expr), value)`.

Builtin            | Return type          | Returns
-------------------|----------------------|----------
fun                | String literal       | Function name
file               | String literal       | Source file
line               | String literal       | Source line
lineno             | Integer literal      | Source line number
count(args)        | Integer literal      | Parameter count
off_of(ident)      | Integer literal      | Variable stack offset
len_of(ident)      | Integer literal      | Element count of the array
size_of(ident)     | Integer literal      | Variable size
type_of(expr)      | String literal       | Expression type
strfy(expr)        | String literal       | String representation of expr
cast("type", expr) | Any                  | The expression cast to type
literal(lit, ...)  | Void                 | The arguments merged as a literal
asm("statement")   | Void                 | -

```txt
# Source code (before parsing)
fun main(): int64
    let a: int8* = 0
    printf("size_of(a): %lld", size_of(a))
    printf("%s:%s: Test", file, fun)
    assert_extra(a != 0, line, file, lineno)
    ret 0
end

# AST representation (after parsing)
# Command: "python src/Main.py -i tests/builtins/main.ml -d"
fun main()
  ((int8*)(main_a) = 0)
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
\|\|   | Binary | -        | Logical or
&&     | Binary | -        | Logical and
==     | Binary | -        | Comparison (Equals)
!=     | Binary | -        | Negated comparison (Not equals)
<=     | Binary | -        | Less-than-or-equal comparison
\>=    | Binary | -        | Greater-than-or-equal comparison
<      | Binary | -        | Less-than comparison
\>     | Binary | -        | Greater-than comparison
&      | Unary  | Prefix   | Address
^      | Unary  | Prefix   | Function address
\*     | Unary  | Prefix   | Dereference

Precedence | Operator | Description
-----------|----------|------------
Level 0    | `^`                         | Function address
Level 1    | `cast` `type_of` `len_of` `size_of` `count` `literal` `asm` `()` `.` | Builtins, function calls, macro calls and element access
Level 2    | `*` `&`                     | Address and dereference
Level 3    | `at`                        | Array element access
Level 4    | `*` `/`                     | Multiplication and division
Level 5    | `+` `-`                     | Addition and subtraction
Level 6    | `%` `&` `\|`                | Remainder, bitwise and, bitwise or
Level 7    | `==` `!=` `>` `<` `>=` `<=` | Comparisons
Level 8    | `&&` `\|\|`                 | Logical and, logical or
Level 9    | `... if ... else ...`       | Ternary conditional
Level 10   | `=`                         | Assignment
Level 11   | `,`                         | Comma

## Inline assembly

> [!WARNING]
> The `asm` builtin does not validate any inline assembly code passed as a parameter (by design). Thus, manually shrinking or growing the function stack leads to undefined behavior.

```txt
asm ".macro stack_snapshot"
asm "   push %r9"
asm "   push %r8"
asm "   push %rcx"
asm "   push %rdx"
asm "   push %rsi"
asm "   push %rdi"
asm ".endm"
...

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

## Aliases

> [!Note]
> The alias statement defines alternative names for existing types and variables, structures and functions.
> The type aliases defined below are part of the standard library. (`stdlib/c/cdefs.ml`)

```txt
# Alias syntax
# alias alternative_name = name
# alias alternative_type = type

alias c_void = void
alias c_char  = int8
alias c_short = int16
alias c_int   = int32
alias c_long  = int32
alias c_long_long = int64
alias c_str = int8*
alias c_stream = FILE*
```

## Declaration/Assignment

```txt
# Declaration syntax
# Recommended naming convention: snake_case
# Explicit type definitions are optional, except for arrays, heredocs, and signatures. (type inference).
let variable: type = value
let pointer: type* = address
let signature: fun(_: type_1, ..., _: type_n) = ^function
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
#
# if <condition>
#    <if_body>
# elif <condition2>
#    <elif_body>
# ...
# else
#    <else_body>
# end

if a + 5 > 20
    a = 30
elif a + 15 == 20
    a = 20
else
    a = 10
end
```

## While loops

```txt
# While loop syntax
#
# while <condition>
#    <while_body>
# end

while a >= 10
    a = a / 10
end
```

## For loops

For loops are used to iterate over a sequence using iterators.

```txt
# For loop syntax
#
# for <iter> in <target>
#    <for_body>
# end

for it in range(15)
    println(it)
end
```

### Internal representation

```txt
<iter-ret> <target> = iter(&<target_expr>)
<start-ret> <it> = iter(&<target>)
for(<it> = start(<it>); stop(&<it>) == false; <it> = next(&<it>)) {
    <body>
}
```

### Extensibility

To extend for loops for custom types, declare the required `iter`, `start`, `stop` and `next` methods, operating on references to the given type.

```txt
# For-loop support for range type

fun iter(arg: range&): range&
    ret &arg
end

fun start(arg: range&): int64
    ret arg.range_start
end

fun stop(arg: range&): bool
    ret arg.range_idx < arg.range_stop
end

fun next(arg: range&): int64
    arg.range_idx = arg.range_idx + 1
    ret arg.range_idx
end

```

## Import statements

> [!TIP]
> Importing ML files from a parent directory can only be achieved by adding that directory to the include path of the ML compiler using the `-I` option (`python Main.py -I <PATH_TO_DIR> ...`)

```txt
# Import statement syntax
# Note: This instructs the compiler to include mymodule (`mymodule.ml`) in the build.
import mymodule
import dir.dir2.othermodule
```

## Multi-line statements

```txt
# Expression-based statements
(str("Hello ").
    concat(str("World!")).
    print)

# Function statement (example)
fun
myfunc
(arg1: int64, arg2: int64): int64
    ret arg1 + arg2
end
```

For expression-based statements and array declarations, the compiler checks whether every parentheses and square brackets have been properly closed. If not, the compiler continues to the next line. However, for all other unterminated statements this check is done automatically.

## Namespace statements

```txt
# Namespace statement syntax
namespace mynamespc
    let var = 15

    fun greet(name: int8*): void
        println("Hello ", name, "!")
    end
end

# Namespace member access
mynamespc.var = 20
mynamespc.greet("You")
```

## Defer statements

> [!TIP]
> The `defer` statement is particularly useful for resource clean-up, such as freeing allocated memory, closing files or running cleanup tasks at the end of the function scope.

```txt
# Source code (before parsing)
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

## Structures

> [!TIP]
> For each defined struct the compiler automatically inserts a constructor-like function with the same name as the struct.

> [!WARNING]
> Currently struct elements block the declaration of identifiers with the same name.
> This is a bug and will be fixed soon.

```txt
# Struct syntax
# struct name
#   memb1: type
#   ...
#   membn: type
#
# end

struct mystring
    len: int64
    cptr: int64*
end

fun main: int32
    # Struct object declaration
    let obj: mystring
    let obj2 = mystring(3, "Hel")

    # Triggers a redeclaration error for cptr
    let cptr = 15
end
```

## Macros

MiniLang's macro system stands out as its most exceptional feature, surpassing all other systems languages. With the ability to manipulate the Abstract Syntax Tree (AST) directly at compile time, macros enable dynamic structural modifications and transformations. This capability offers powerful meta-programming features akin to those found in Lisp. A detailed description of the MiniLang macro system can be found [here](docs/language/rethinking%20macros.md).

```txt
# Macro syntax
# macro mymacro
# macro mymacro(arg1, arg2, arg3, ...)

macro int(_expr)
    cast("int", _expr)
end

# The supports C++-like type casts trough macros
let myint = int(50)
```

> [!NOTE]
> Macros are variadic by default. Thus, the last argument of a macro accepts a variable number of expressions.
> The macro argument count can be determined by using the `count` builtin. This feature is particularly useful for passing the parameter count to a variadic function.

```txt
macro max(args)
    _max(count(args), args)
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

### Function signatures (function pointers)

ML refers to function pointers as `function signatures`. Functions can have multiple signatures which can be bound to a variable by using the `^` (function address) operator.

```txt
import stdlib.io.print

fun test(arg: int8*): int8&
    ret arg
end

fun test_ptr(farg: fun(_: int8*): int8&, arg: int8*): void
    println(farg(arg))
end

fun main
    let c: int8 = 10
    let x: fun(_: int8*): int8& = ^test
    test_ptr(^x, &c)

    ret 0
end
```

### Function overloading

> [!WARNING]
> Currently function overloading does cannot infer functions solely based on their return types.

Function overloading enables the creation of multiple functions with the same name, distinguished by their different parameter types or counts.

```txt
fun _print(arg: int64): void
    printf("%lld", arg)
end

fun _print(arg: int8*): void
    printf("%s", arg)
end

fun _print(arg: void*): void
    printf("%p", arg)
end
```

### Uniform function call syntax (UFCS)

Uniform Function Call Syntax (UFCS) enables calling standalone functions using method call syntax on the objects they operate on. It behaves similar to the pipe operator found in other languages, enabling a more fluid and expressive way to chain function calls.

```txt
let mystr = str("Hello")

# Is equivalent to:
# print(len(concat(mystr, " World!")))
mystr.concat(" World!").len.print
```

## RAII

> [!WARNING]
> In the case where a composite type is missing the `copy` method, the intent defaults to moving (surrendering the ownership) the resource to the function. The compiler warns against these implicit ownership claims.

> [!WARNING]
> Due to the current scope implementation references to rvalues (function return values) are not cleaned up. This is a bug and will be resolved soon.

RAII (Resource Acquisition Is Initialization) is a memory allocation tehnique where resources like memory, files, or locks are automatically managed by associating their acquisition and release with the lifetime of an object.

In ML, RAII determines the lifetime of the composite types. Resources are destructed by calling their associated `destruct` and copied by calling `copy`. Both aforementioned methods operate on references of the resources' type. The `move` builtin allows createing rvalue references of resources.

> [!IMPORTANT]
> Implicit copying occurs only for parameters of a function call.

Description   | Type (var)       | Notation     | Effect
--------------|------------------|--------------|-------
Implicit copy | composite        | `var`        | `copy(&var)`
Explicit copy | reference        | `&copy(var)` | `&copy(&var)`
Implicit move | rvalue reference | `var`        | `var`
Explicit move | composite        | `move(var)`  | `var`
Reference     | reference        | `&var`       | `&var`
