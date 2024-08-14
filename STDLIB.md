# Standard library

An overview of the ML standard library.

## Motivation

The standard library permits the use of both unsafe c standard library functions (for embedded systems and nostalgic c programmers) and their safe ML counterparts, plus some other useful modern libraries, like `string` and `convert`.

## Modules

> [!TIP]
> Click on a module to display its documentation.

Module                            | Parent dir.   | Description
----------------------------------|---------------|------------
[cdefs](docs/stdlib/cdef.md)      | c             | Commonly used c type definitions
[cstdlib](docs/stdlib/cstdlib.md) | c             | Bindings for ported functions of the c standard library
[cstarg](docs/stdlib/cstdarg.md)  | c             | Bindings for the `stdarg.h` c library
[print](docs/stdlib/print.md)     | io            | Extendable and safe frontend for `printf`/`fprintf`
read          | io            | Extendable and safe frontend for `scanf`/`fscanf`
fio           | io            | A frontend for c file-related functions
convert       | -             | Type conversion library
debug         | -             | Rust-like assertables and panic macros
misc          | -             | Miscelaneous macros and functions (for macro)
[string](docs/stdlib/string.md)   | -             | Functional-like string library
backend       | string        | Bindings for the `sds.h` library (Simple Dynamic Strings)
va_utils      | legacy        | Simplistic `stdarg.h`-like implementation for the assembly backend
