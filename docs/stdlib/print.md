# IO print library

Source: [include/stdlib/io/print.ml](../../include/stdlib/io/print.ml)

Extendable and safe frontend for `printf`/`fprintf`.

## Functions

Function   | Description
-----------|------------
`_print`   | `print` handlers that call `printf` based on the argument type

## Macro

Macro      | Description
-----------|------------
print      | Prints arguments to `stdout`
println    | Prints arguments to `stdout`, followed by newline
print_to   | Prints arguments to the specified stream
println_to | Prints arguments to the specified stream, followed by newline

## Extensibility

> [!IMPORTANT]
> To extend `print` or any of the macros, simply declare a new `_print` helper with a `stream` argument and an argument of the custom type to extend.

```txt
import stdlib.c.cdef
import stdlib.io.print

struct exstruct
    cnt: int64
    cptr: void*
end

fun _print(st: c_stream, arg: exstruct): void
    print_to(st, "exstruct(cnt=", arg.cnt, ", cptr=", arg.cptr, ")")
end

fun main: int32
    exstruct(11, null).print
    ret 0
end
```
