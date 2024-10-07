# Rethinking macro systems

## Prelude

In systems programming languages, macros are often seen as an unsafe tool for code generation, implemented as a standalone metaprogramming system that operates separately from the main parsing phase. This separation limits their ability to perform deeper structural changes, like AST (Abstract Syntax Tree) manipulation, leading to potential issues with readability, safety, and optimization.

This incoplete integration has influenced many newer system languages, perpetuating the view that macros are inherently problematic and something to be avoided. However, the problem lies not with the concept of macros, but with the way they are integrated into the language.

Take Rust and Zig, for example. Rust advances beyond C/C++ by ensuring its macros are hygienic, type-safe, and predictable, but it restricts their metaprogramming capabilities by expanding them only after the parsing phase. Zig, on the other hand, avoids macros altogether in favor of simplicity and predictability.

It's time to rethink metaprogramming from the ground up, shedding the negative stigma surrounding macros and recognizing that a well-integrated macro system can enhance both safety and expressiveness in systems languages.

## Language design

The language must integrate seamlessly with its macro system, requiring modifications that differ from those found in traditional systems programming languages.

### Type-aware AST

Each node of the AST is associated with a type. This includes `if`, `while`, `for` statemens, variable and function declarations.  These control flow structures are of void type and can be seamlessly inserted into expressions through macros, allowing flexible code manipulation.

```txt
macro if_else(_cond, _if_true, _if_false)
    if _cond
        _if_true
    else
        _if_false
    end
end

fun main
    let a = 10

    # The if statement is used inside an expression via `if_else`
    if_else(a > 5, 
        print("Greater"),
        print("Lower")
    )

    ret 0
end
```

### Unified syntax model

A **statement list** refers to an expression or a comma-separated list of expressions.

An **argument list** refers to a specialized form of statement lists used to represent function call arguments, though structurally identical to statement lists.

Compound statements consist of newline-separated statements. Despite their slightly different AST structure, they can be normalized by the compiler and used in place of either statement lists or argument lists. Normalization is not covered as it's not relevant to the topic.

This visual representation shows the human-readable structure of the terms:

```txt
# Argument and statement list structure
# Optimized for argument extraction
# fun(1, 2, 3)
    FUN_CALL(add)
          |
         GLUE
        /   \
     GLUE    3
    /   \
 GLUE    2
    \    
     1

# Compound statement structure
# Optimized for space
# 1 2 3 (separated by newline)
        GLUE
       /    \
   GLUE      3
  /    \
 1      2
```

This example demonstrates the distinction between the terms:

```txt
import stdlib.io.print

fun add(term1: int64, term2: int64)
    ret term1 + term2
end

fun main
    # main's function body is a compound statement
    let term1 = 0
    let term2 = 0

    # The statement below is a statement list
    # A statement is also considered a single-element statement list
    (term1 = 15), (term2 = 16)

    # (term1, term2) constitutes the argument list passed to add
    print(add(term1, term2))
    ret 0
end
```

The parser allows statement lists, argument lists and compound statements can be used interchangably thanks to their structural equivalence, which yeilds identical results when traversing in a depth-first manner.

### Argument list normalization

For functions and macro calls, the compiler normalizes the argument list by merging nested argument lists.

This example demonstrates argument list normalization:

```txt
macro add_args
    15, 16
end

macro print_args
    14, add_args, 17
end
```

```txt
print_args before normalization:

            GLUE
           /    \
        GLUE    17
       /    \
    GLUE     GLUE
       \    /    \
       14 GLUE    16
              \
              15 

print_args after normalization:

            GLUE
           /    \
        GLUE    17
       /    \
    GLUE     16
   /    \
GLUE     15
    \
    14
```

### Builtins

Builtins are macro-like constructs that are built into compiler. MiniLang offers 2 main builtins that are particularly useful in combination with macros.

The `count(args)` builtin returns the number of arguments within an argument list. It allows macros to pass the argument count to variadic macros and to provide variadic macro constraints (discussed later).

The `group(args)` builtin allows to escape argument normalization, which is used to pass multi-element statement lists as macro arguments.

## Macro design

MiniLang macros operate on argument lists and produce compound statements. These macros can directly replace and transform statement lists, argument lists, and allow compound statements within expressions. Macros as considered "lazy" as they are expanded and checked at the call site.

### Result macros

MiniLang provides a special type of macro known as result macros. The last expression (not a statement list) within the macro's body is inserted directly into the expression where the macro is expanded, while the rest of the body is hoisted above this expression. This feature is particularly useful for returning values from compound statements, which are of `void` type and can't be returned in normal circumstances.

Developers should exercise caution with result macros like last. For example, `last(1, 2, 3)` returns `3`, not the entire statement list `(1, 2, 3)`. To enforce returning a grouped expression, developers can use the `group` builtin.

```txt
# Normal macro
macro _last(_args)
    args
end

# Result macro
macro ret last(_args)
    _args
end

# Result macro wich returns the digit count of a number
macro ret digit_count(_cnt, _num)
    _cnt = 0
    while _num > 0
        _cnt = _cnt + 1
        _num = _num / 10
    end
    _cnt
end
```

### Variadic macros

Macros are variadic by default to provide a fallback mechanism. This means that the last argument of the macro accepts a statement list. Since macros are greedy, when the argument count of the macro exceeds the expected count, the overload with the highest argument count will be used. The other overloads, which have a smaller argument count, will receive exactly the number of arguments they are designed to accept.

To guarantee that the overload with the highest argument count receives exactly the number of arguments requested, this can be checked during runtime using assert or panic in combination with a `count` builtin.

In this example, if `sum4` is called with a different number of arguments than expected, `assert` will trigger an error, ensuring that the macro behaves correctly and predictably.

```txt
# Guaranteed to recieve 2 arguments
macro sum(_arg1, _arg2)
    _arg1 + _arg2
end

# No guarantee on the number of arguments
macro sum(_arg1, _arg2, _arg3)
    _arg1 + sum(_arg2, _arg3)
end

# Runtime guarantee to recieve 4 arguments
macro ret sum4(_args)
    assert(count(_args) == 4)
    sum(_args)
end
```

### Parsing process

Macros are evaluated using a 2-step parsing process. On macro declaration, the compiler creates placeholders for the parameters (type-agnostic parsing) and checks for syntactical and type violations of the expressions and constructs which can be deducted (which do not involve the parameters). At the call site the expansion the parser directly substitutes the placeholders with the provided parameters and performs the remaining checks.

## Macro overloading

Macro signatures are distinguised based on the argument count. The signature with the highest argument count is preffered (greedy). The argument count is determined dynamically after normalization.

### Macro recursion

Recursion is enabled in the macro system because of the "lazy" nature of macros and the support for macro overloading. Recursive macros can have multiple signatures, with one or more overloads serving as base cases. This behavior is akin to fold or reduce operations, where the argument list is gradually reduced while simultaneously expanding the output.

Consider the reverse macro from the standard library. The base case of this macro accepts exactly two arguments. Since macros are variadic by default, any argument list with more than two arguments will group the additional arguments into a statement expression and bind them to `_arg3`.

When `reverse(_arg2,_arg3)` is called, the argument list is normalized, and the new arguments are bound accordingly. Here, the old `_arg2` becomes `_arg1`, and `_arg2` is taken from the previous `_arg3`, effectively removing one element from the old `_arg3` (now referred to as the new `_arg3`).

```txt
# Reverses the argument list
macro reverse(_arg, _arg2)
    _arg2, _arg
end
macro reverse(_arg1, _arg2, _arg3)
    reverse(_arg2, _arg3), _arg1
end
```

## Examples

Now that we have designed a simple, yet powerful and flexible macro system, let's go over some examples that demonstrate the claims of the document.

### Argument list modification

```txt
# Inserts a delimiter between arguments
macro delimit(_delim, _arg)
    _arg
end
macro delimit(_delim, _arg, _arg2)
    _arg, _delim, _arg2
end
macro delimit(_delim2, _arg, _arg2, _other)
    delimit(_delim2, _arg, _arg2), _delim2, delimit(_delim2, _other)
end
```

This example showcases the `delimit` macro, which modifies argument lists by inserting a specified delimiter between each provided arguments.

### Variadic wrapper

```txt
# Print helper functions
# !Edited out, can be found at stdlib.io.print

# Convenience macros
macro print(_arg)
    _print(stdout, _arg)
end
macro print(_arg, _other)
    print(_arg)
    print(_other)
end
```

This example introduces a variadic wrapper for `print` functionality, allowing the user to print multiple types of data to the console. The print macro calls the `_print` function helper to output the argument based on its type using function overloading. Thus, we gain access to a type-safe `printf` alternative.

### Variadic function helper

```txt
fun _max(cnt: int64, ...): int64
    let list: va_list
    va_start(list, cnt)

    let mx = 0
    let arg = 0
    for idx in range(cnt)
        arg = va_arg_int64(list)
        if arg > mx
            mx = arg
        end
    end

    ret mx
end

# Wrapper of the variadic function
macro max(args)
    _max(count(args), args)
end
```

In this example, a variadic function is defined to find the maximum value among a list of integers. The `max` macro acts as a helper, enabling users to pass the argument count to the variadic function helper `_max`, demonstrating how macros can improve interactions with variadic functions.

### Construct creation

```txt
import stdlib.io.read
import stdlib.io.print

let falltrough = false
macro switch(_ident2, _cond2, _body2)
    if (_ident2 == _cond2) || falltrough
        falltrough = true
        _body2
    end

end

macro switch(_ident, _cond, _body, _other)
    switch(_ident, _cond, _body)
    switch(_ident, _other)
end

macro break
    falltrough = false
end

fun main
    let a = 0
    read(a)

    switch(a,
        (15, 
            group(
                print("Is 15"), 
                break)),
        (16, 
            group(
                print("Is 16"), 
                print("Also 16"))), 
        (17, 
            print("Is 17")),
        (18, 
            print("Is 18")),
        (19, 
            print("Is 19")),
        (20, 
            print("Is 20"))
    )
    ret 0
end
```

This example demonstrates how the macro system allows developers to create new constructs, such as the `switch` statement.

### Customizable Allocation

```txt
import stdlib.c.cdef
import stdlib.c.cstdlib
import stdlib.debug
import stdlib.alloc.backend

literal("#define ML_ALLOC_GC")

# Indicates whether the gc is active
let _gc_running = false

macro alloc_warn
    printf("Allocation defaults to malloc in %s:%s. Consider starting the gc by using alloc_start.\n", fun, file)
end

macro alloc_stop
    if _gc_running == false
        panic("Cannot stop an already stopped gc.")
    end

    literal("#undef s_malloc")
    literal("#undef s_realloc")
    literal("#undef s_free")
    literal("#define s_malloc malloc")
    literal("#define s_realloc realloc")
    literal("#define s_free free")
    literal("#include <sdsalloc.h>")

    gc_stop(&ml_gc)
    _gc_running = false
end

macro alloc_start(_lit)
    if _gc_running
        panic("Cannot start an already running gc.")
    end

    literal("#undef s_malloc")
    literal("#undef s_realloc")
    literal("#undef s_free")
    literal("#define s_malloc ml_malloc")
    literal("#define s_realloc ml_realloc")
    literal("#define s_free ml_free")
    literal("#include <sdsalloc.h>")

    gc_start(&ml_gc, &_lit)
    _gc_running = true
    defer alloc_stop
end

fun alloc_size(sz: int64, fill: bool): void*
    let ptr = null
    if _gc_running
        ptr = _malloc(sz)
    else
        ptr = malloc(sz)
        alloc_warn
    end

    if ptr == null
        panic("Allocation failed.")
    end

    if fill
        memset(ptr, 0, sz)
    end

    ret ptr
end

fun alloc_size(size: int64): void*
    ret alloc_size(size, false)
end

macro alloc(_lit)
    _lit = alloc_size(size_of(_lit))
end

macro alloc(_lit, _size)
    _lit = alloc_size(_size)
end

macro alloc(_lit, _num, _size)
    _lit = alloc(_num, _size * _num)
end

macro alloc_zeroed(_lit)
    _lit = alloc_size(size_of(_lit), true)
end

macro alloc_zeroed(_lit, _size)
    _lit = alloc_size(_size, true)
end

macro dealloc(_lit)
    if _gc_running
        _lit._free
    else
        _lit.free
    end
    _lit = null
end

macro with(_lit, _body)
    alloc(_lit)
    defer dealloc(_lit)
    _body
end
```

This example demonstrates a flexible memory allocation system that allows developers to choose between garbage collection or standard malloc-based allocation.

#### Convenience

Developers don’t need to explicitly use the `size_of` builtin; the macro handles it automatically, streamlining the allocation process.

#### Customizable Behavior

The `alloc_start` and `alloc_stop` macros manage the gc. When active, memory allocation switches to `ml_malloc`, `ml_realloc`, and `ml_free` (garbage-collected). If the GC is inactive, standard `malloc`, `realloc`, and `free` functions are used for allocation.

#### Error Handling

The system includes runtime checks to prevent incorrect gc usage. It ensures the gc isn’t started twice or stopped when it’s not running, triggering custom error messages if these rules are violated.

#### Customizable Warnings

If the gc is inactive, the `alloc_warn` macro triggers a warning, indicating that the default allocation (using `malloc`) is in effect. Developers can override this behavior by defining their own version of the macro with the same name and argument count, thanks to the lazy-evaluated nature of macros.
