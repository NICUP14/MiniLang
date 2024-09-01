# Allocation library

Source: [include/stdlib/builtin/alloc.ml](../../include/stdlib/builtin/alloc.ml)

Provides customizable memory allocation utilities.

## Macros

Macro                       | Description
----------------------------|------------
`alloc_warn`                | Default warning for non-gc allocation.
`alloc_stop`                | Stops the garbage collector.
`alloc_start(_lit)`         | Starts the garbage collector, `_lit` points to the stack bottom.
`alloc(_lit)`               | Assigns `_lit` to an allocated memory block based on its size.
`alloc(_lit,_size)`         | Assigns `_lit` to an allocated memory block of size `_size`.
`alloc_zeroed(_lit)`        | Assigns `_lit` to an zero-filled allocated memory block based on its size.
`alloc_zeroed(_lit, _size)` | Assigns `_lit` to an zero-filled allocated memory block of size `_size`.
`dealloc(_lit)`             | Deallocates the memory block pointed by `_lit` and assigns `_lit` to null.
`with(_lit,_body)`          | Creates a block in which `_lit` is allocated, used by `_body`, then deallocated.

## Functions

Function     | Description
-------------|------------
`alloc_size` | Allocates a memory block of the given size, filled based the `fill` flag.

## Warnings

> [!WARNING]
> Memory allocated by the `alloc` utilites use different allocators than the one provided by the c standard library. Thus, calling `free` on a memory address allocated by `alloc` causes undefined behaviour.
