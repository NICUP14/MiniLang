# String library

Source: [include/stdlib/string.ml](../../include/stdlib/string.ml)

Provides a functional-like ML frontend of the sds c library. The functions behave like pure ones.

**Check out [sds](https://github.com/antirez/sds)**, the string library couldn't be made possible without without this c library.

## Aliases

Alias | Alias of
------|---------
str   | sds

## Functions

Function      | Description
--------------|------------
str           | Creates a new string starting from a null terminated C string
str_from      | Creates a new string starting from a printf-alike format specifier
empty_str     | Creates an empty (zero length) string
extend        | Extends the string to the given length
clone         | Duplicates the given string
clear         | Clears the given string (in-place)
copy          | Copies one string to the other
len           | Returns the length of the string
substr        | Returns the substring pointed by the indices
concat        | Append the latter string to the first
concat_from | Append the string obtained from a format specifier to the first
trim          | Remove the part of the string from left and from right composed just of chars found in the second c string
compare       | Compare two sds strings s1 and s2 with memcmp
to_lower      | Apply tolower to every character of the string
to_upper      | Apply toupper to every character of the string
find          | Returns the index of the first occurence of `sub` in `s`
split         | Split a string with the given separator. Returns an array of strings
join          | Joins an array of C strings using the specified separator and returns the result
to_str        | Creates strings from different types

## Macros

Macro | Description
------|------------
c_str | Converts the argument to a c string using `cast`

## Warnings

> [!WARNING]
> Functions of sds c library are not pure, unlike their ML counterparts.

> [!WARNING]
> Relies on the sds bindings for ML (string-backend.ml).
