# convert.ml - Conversion library for ml.
# Provides a ML frontend for converting between types found in stdlib.

literal("#include <errno.h>")

import stdlib.debug
import stdlib.string
import stdlib.c.cdef
import stdlib.c.cstdlib

# Provides bindings for the c 'errno' variable, cast to int64.
macro c_errno
    cast("int64", literal("errno"))
end

# Represents the c 'ERANGE' error code, cast to int64.
macro c_ERANGE
    cast("int64", literal("ERANGE"))
end

# Represents the minimum value for a c long integer, cast to int64.
macro c_LONG_MIN
    cast("int64", literal("LONG_MIN"))
end

# Represents the maximum value for a c long integer, cast to int64.
macro c_LONG_MAX
    cast("int64", literal("LONG_MAX"))
end

# Represents the minimum value for a c long long integer, cast to int64.
macro c_LLONG_MIN
    cast("int64", literal("LLONG_MIN"))
end

# Represents the maximum value for a c long long integer, cast to int64.
macro c_LLONG_MAX
    cast("int64", literal("LLONG_MAX"))
end

# Converts an int64 value to int64 (no-op). This function is provided for consistency with the overloaded versions.
fun to_int64(arg: int64): int64
    ret arg
end

# Converts a c string to an int64 value. Performs additional checks to ensure the string represents a valid integer.
#
# Panics:
# * If the string is null.
# * If the string is empty or starts with whitespace.
# * If the conversion causes a range error (ERANGE).
# * If the string contains non-numeric characters.
fun to_int64(s: c_str): int64
    if s == null
        panic("String is null")
    end

    if (s[0] == '\0' || isspace(s[0]) > 0)
        panicf("String '%s' is not a number (check #1)", s)
    end

    let term: c_str = null
    let l = strtoll(s, &term, 0);

    if (l == 0 && c_errno == c_ERANGE)
        panicf("String '%s' to integer causes a range error", s)
    end
    if (*term != '\0')
        panicf("String '%s' is not a number (check #2)", s)
    end

    ret l
end

# Converts a string to an int64.
fun to_int64(s: str): int64
    ret to_int64(c_str(s))
end

# Converts an int64 to a boolean value (true for non-zero).
fun to_bool(arg: int64): bool
    ret true if arg == cast("int64", true) else false
end

# Converts a c string to a boolean.
fun to_bool(s: c_str): bool
    if strcmp(s, "true") == 0
        ret true
    elif strcmp(s, "false") == 0
        ret false
    else
        panic("Cannot convert string")
    end
end

# Converts a string to a boolean.
fun to_bool(s: str): bool
    ret to_bool(c_str(s))
end

# Converts an int64 to an int8.
fun to_int8(arg: int64): int8
    ret cast("int8", arg)
end

# Converts a c string to an int8.
fun to_int8(s: c_str): int8
    ret cast("int8", to_int64(s))
end

# Converts a string to an int8.
fun to_int8(s: str): int8
    ret to_int8(c_str(s))
end

# Converts an int64 to an int16.
fun to_int16(arg: int64): int16
    ret cast("int16", arg)
end

# Converts a c string to an int16.
fun to_int16(s: c_str): int16
    ret cast("int16", to_int64(s))
end

# Converts a string to an int16.
fun to_int16(s: str): int16
    ret to_int16(c_str(s))
end

# Converts an int64 to an int32.
fun to_int32(arg: int64): int32
    ret cast("int32", arg)
end

# Converts a c string to an int32.
fun to_int32(s: c_str): int32
    ret cast("int32", to_int64(s))
end

# Converts a string to an int32.
fun to_int32(s: str): int32
    ret to_int32(c_str(s))
end

# "I don't care about types!" conversions
macro boolean(_expr)
    to_bool(_expr)
end
macro number(_expr)
    to_int64(_expr)
end
macro string(_expr)
    to_str(_expr)
end