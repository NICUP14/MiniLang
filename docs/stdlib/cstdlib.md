# C standard library

Source: [include/stdlib/c/cstdlib.ml](../../include/stdlib/c/cstdlib.ml)

Provides bindings for ported functions of the c standard library.

## Functions

| Function | Description
|----------|------------
| `abs`    | Returns the absolute value of an integer
| `atoi`   | Converts a c string (`int8*`) to an integer
| `exit`   | Cleans resources and terminates the calling process immediately
| `fprintf`| Writes a formatted c string (`int8*`) to a specified file stream
| `free`   | Deallocates the memory previously allocated by `malloc`, `calloc`, or `realloc`
| `fscanf` | Reads formatted input from a file stream
| `getchar`| Reads the next character from standard input
| `isdigit`| Checks if a character is a digit ('0' to '9')
| `isspace`| Checks if a character is a whitespace character
| `malloc` | Retuns a pointer to `size` bytes of uninitialized storage
| `memcpy` | Copies `count` bytes from the object pointed to by `src` to the object pointed to by `dest`
| `memset` | Fills a block of memory with the specified value
| `printf` | Writes a formatted c string to standard output
| `puts`   | Writes a c string to standard output, followed by newline
| `realloc`| Reallocates previously allocated memory to a new size
| `scanf`  | Reads formatted input from standard input
| `strcat` | Appends one c string to the end of another
| `strchr` | Searches for the first occurrence of a character in a c string
| `strcmp` | Compares two c strings lexicographically
| `strcpy` | Copies one c string to another
| `strdup` | Duplicates a c string by allocating memory for the new one
| `strlen` | Returns the length of a c string
| `strncat`| Appends a specified number of characters from one c string to another
| `strncmp`| Compares a specified number of characters from two c strings
| `strncpy`| Copies a specified number of characters from one c string to another
| `strrchr`| Searches for the last occurrence of a character in a c string
| `strstr` | Finds the first occurrence of a substring in a c string
| `strtoll`| Converts a c string to `int64` (`long long int`)

## Warnings

> [!WARNING]
> The c standard library provided by ML is currently incomplete. To port a c standard library function ML, simply declare an external function with the same name as the c one along with its appropriate parameters and their ML-equivalent types.
> If such task interests you, please fork the project and add the required bindings along with the updated documentation and submit a pull request.
