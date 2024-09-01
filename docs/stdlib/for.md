# For loop utilities

Source: [include/stdlib/builtin/for.ml](../../include/stdlib/builtin/for.ml)

Provides convenient for-based constructs and looping utilities.

## Types

Types         | Description
--------------|------------
`range`       | Type to hold range-based looping information.
`file_range`  | Type to hold file-based looping information.
`c_str_range` | Type to hold string-based looping information.

## Functions

> [!NOTE]
> `iter`/`start`/`stop`/`next` methods are not discussed in this document. Check the [standard library examples](examples.md) for-based loop examples.

Functions | Description
------|------------
range | Creates an iterator to a sequence of numbers based on the `start` and `stop` (optional) values.
lines | Creates an iterator to a sequence of lines from the given file.
