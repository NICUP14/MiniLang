# convert.ml - Conversion library for ml.
# Provides a ML frontend for converting between types found in stdlib.
# WARNING: The `to_str` conversion method is provided by `stdlib/string.ml`

literal("#include <errno.h>")

import stdlib.c.cstdlib
import stdlib.debug
import stdlib.defs

macro c_errno
    cast("int64", literal("errno"))
end
macro c_ERANGE
    cast("int64", literal("ERANGE"))
end
macro c_LONG_MIN
    cast("int64", literal("LONG_MIN"))
end
macro c_LONG_MAX
    cast("int64", literal("LONG_MAX"))
end
macro c_LLONG_MIN
    cast("int64", literal("LLONG_MIN"))
end
macro c_LLONG_MAX
    cast("int64", literal("LLONG_MAX"))
end

fun to_int64(arg: int64): int64
    ret arg
end

fun to_int64(s: cstr): int64
    if s == null
        panic("String is null")
    end

    if (s[0] == '\0' || isspace(s[0]) > 0)
        panicf("String '%s' is not a number (check #1)", s)
    end

    # c_errno = 0;
    let stop: cstr = null
    let l = strtoll(s, &stop, 0);

    if (l == 0 && c_errno == c_ERANGE)
        panicf("String '%s' to integer causes a range error", s)
    end
    if (*stop != '\0')
        panicf("String '%s' is not a number (check #2)", s)
    end

    ret l
end

fun to_bool(arg: int64): bool
    ret true if arg == cast("int64", true) else false
end

fun to_bool(s: cstr): bool
    if strcmp(s, "true") == 0
        ret true
    elif strcmp(s, "false") == 0
        ret false
    else
        panic("Cannot convert string")
    end
end

fun to_int8(arg: int64): int8
    ret cast("int8", arg)
end

fun to_int8(s: cstr): int8
    ret cast("int8", to_int64(s))
end

fun to_int16(arg: int64): int16
    ret cast("int16", arg)
end

fun to_int16(s: cstr): int16
    ret cast("int16", to_int64(s))
end

fun to_int32(arg: int64): int32
    ret cast("int32", arg)
end

fun to_int32(s: cstr): int32
    ret cast("int32", to_int64(s))
end