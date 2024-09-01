# IO read library

Source: [include/stdlib/io/read.ml](../../include/stdlib/io/read.ml)

Extendable and safe frontend for `scanf`/`fscanf`.

## Functions

Function   | Description
-----------|------------
`_read`   | `read` handlers that call `fscanf` based on the argument type

## Macros

Macro     | Description
----------|------------
input     | Reads a string (`str`, not `c_str`) from `stdin` until a newline is found
read      | Reads values from `stdin` and updates its arguments
read_from | Reads values from the given stream and updates its arguments

## Extensibility

> [!IMPORTANT]
> To extend `read` or any of the macros, simply declare a new `_read` helper with a `c_stream` argument and a pointer to the custom type to extend.

## Warnings
