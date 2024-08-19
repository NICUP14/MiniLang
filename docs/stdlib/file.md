# IO File library

Source: [include/stdlib/io/file.ml](../../include/stdlib/io/file.ml)

Provides a frontend for c file-related functions.

## Functions

Function  | Description
----------|------------
open_file | Opens a file identified by `filename` in the given file acces mode (`mode` defaults to read mode)
read_line | Reads a line from the given stream until a newline or end-of-file is encountered.
read_file | Reads `size` bytes from the file associated with the given stream and returns it in string form. (`size` defaults to file size)

## Macro

Macro      | Description
-----------|------------
close_file | Closes the given file stream

## Warnings

> [!WARNING]
> Failing to close the file stream returned by `open_file` will cause a **dangling file pointer** security issue.
