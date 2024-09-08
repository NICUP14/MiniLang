# C definitions library

Source: [include/stdlib/c/cdef.ml](../../include/stdlib/c/cdef.ml)

Provides ML-equivalents of commonly used c types, type sizes and macros.

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

Macro              | Description
-------------------|------------
`null`             | Null pointer constant
`stdin`            | Standard input stream, used for reading conventional input
`stdout`           | Standard output stream, used for writing conventional output
`stderr`           | Standard error stream, used for writing diagnostic output
`c_ptr_size`       | Size of the `void*` c primitive
`c_char_size`      | Size of the `char` c primitive
`c_short_size`     | Size of the `short` c primitive
`c_int_size`       | Size of the `int` c primitive
`c_long_size`      | Size of the `long` c primitive
`c_long_long_size` | Size of the `long long` c primitive

## Warnings

> [!WARNING]
> The aliased ML-eqivalents of the c types behave like their fixed-length counterparts. Traditional c types sizes are implementation-defined. ML attempts to fix this problem once and for all.
