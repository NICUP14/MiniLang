# C-style variadic function library

Source: [include/stdlib/c/cstdarg.ml](../../include/stdlib/c/cstdarg.ml)

Provides bindings for the `stdarg.h` of the c standard library.

## Types

Type      | Description
----------|------------
`va_list` | Type to hold information about variable arguments (c bind)

## Functions

Function     | Description
-------------|------------
`c_va_start` | Initialize a variable argument list (c bind)
`c_va_arg`   | Retrieve next argument (c bind)
`va_end`     | End using variable argument list (c bind)
`va_arg`     | Wrapper for `c_va_arg` that relies on overloading

## Macros

Macro            | Description
-----------------|------------
`va_start`       | Wrapper for `c_va_start` that mimics the c builtin
`va_arg_voidptr` | Wrapper for `c_va_arg` that returns a `void*` value
`va_arg_int64`   | Wrapper for `c_va_arg` that returns a `int64` value

## Convenience aliases

Alias         | Alias of
--------------|---------
`get_int64`   | `va_arg_int64`
`get_voidptr` | `va_arg_voidptr`

## Example

```txt
import stdlib.io.print
import stdlib.c.cstdlib
import stdlib.c.cstdarg

fun var(argx: int64, ...): void
    # Declares and initializes the variable argument list
    let listx: va_list
    va_start(listx, argx)
    defer va_end(listx)

    # Prints the second argument passed to to function
    listx.get_int64.println
end

fun main: int32
    var(1, 2)
    ret 0
end
```
