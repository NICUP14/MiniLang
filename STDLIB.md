# Standard library

An overview of the ML standard library.

## Motivation

> [!IMPORTANT]
> Ported functions from the c library are regarded as unsafe in terms of type and memory safety, unlike their ML counterparts. Using c bindings should be avoided where safer ML libraries are available.

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
[read](docs/stdlib/read.md)       | io            | Extendable and safe frontend for `scanf`/`fscanf`
[file](docs/stdlib/file.md)       | io            | A frontend for c file-related functions
[convert](docs/stdlib/convert.md) | -             | Type conversion library
[debug](docs/stdlib/debug.ml)     | -             | Customizable rust-like assertables and panic macros
[string](docs/stdlib/string.md)   | -             | Functional-like string library
backend                           | alloc         | Bindings for the `gc.h` c library (Garbage collector)
backend                           | string        | Bindings for the `sds.h` c library (Simple Dynamic Strings)
va_utils                          | legacy        | Simplistic `stdarg.h`-like implementation for the assembly backend (deprecated)
