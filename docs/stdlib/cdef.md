# C definitions library

Source: [include/stdlib/c/cdef.ml](../../include/stdlib/c/cdef.ml)

Provides ML-equivalents of commonly used c types and macros.

## Aliases

Alias        | Alias of
-------------|---------
`c_void`     | `void`
`c_char`     | `int8`
`c_short`    | `int16`
`c_int`      | `int32`
`c_long`     | `int32`
`c_long_long`| `int64`
`c_str`      | `int8*`
`c_stream`   | `FILE*`

## Macros

Macro    | Description
---------|------------
`null`   | Null pointer constant
`stdin`  | Standard input stream, used for reading conventional input.
`stdout` | Standard output stream, used for writing conventional output
`stderr` | Standard error stream, used for writing diagnostic output

## Warnings

> [!WARNING]
> The aliased ML-eqivalents of the c types behave like their fixed-length counterparts. Traditional c types sizes are implementation-defined. ML attempts to fix this problem once and for all.
