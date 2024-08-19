# Conversion library

Source: [include/stdlib/convert.ml](../../include/stdlib/convert.ml)

Provides a ML frontend for converting between types found in stdlib.

## Functions

Function | Description
---------|------------
`to_int64` | Converts an argument to `int64`
`to_bool` | Converts an argument to `bool`
`to_int8(arg: int64)` | Converts an argument to `int8`
`to_int16(arg: int64)` | Converts an argument to `int16`
`to_int32(arg: int64)` | Converts an argument to `int32`

## Warnings

> [!NOTE]
> The `to_str` are part of the string library (`stdlib/string`).
