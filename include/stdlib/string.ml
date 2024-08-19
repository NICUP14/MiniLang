# string.ml - string library for ml.
# Provides a functional-like ML frontend of the sds c library.
# WARNING: Relies on the sds bindings for ML (string-backend.ml).

import stdlib.c.cstdarg
import stdlib.string.backend

alias str = sds

# Returns the underlying null terminated C string.
fun c_str(s: str): int8*
    ret cast("int8*", s)
end

# Create a new sds string starting from a null terminated C string.
fun str(s: int8*): str
    ret sdsnew(s)
end

fun str(s: str): str
    ret str(c_str(s))
end

# Create a new sds string starting from a printf-alike format specifier.
fun str_from(fmt: int8*, ...): str
    let listx: va_list
    va_start(listx, fmt)

    ret sdscatvprintf(sdsempty, fmt, listx)
end

# Create an empty (zero length) sds string. 
# Even in this case the string always has an implicit null term.
fun empty_str: str
    ret sdsempty()
end

fun grow(s: str, size: int64): str
    ret sdsgrowzero(s, size)
end

# Duplicate an sds string.
fun clone(s: str): str
    ret sdsdup(s)
end

# Modify an sds string in-place to make it empty (zero length).
# However all the existing buffer is not discarded but set as free space
# so that next append operations will not require allocations up to the
# number of bytes previously available.
fun clear(s: str): void
    sdsclear(s)
end

# Like sdscpylen() but 't' must be a null-terminated string 
# so that the length of the string is obtained with strlen().
fun copy(s: str, t: str): str
    ret sdscpy(s, c_str(t))
end

# Return the length of the sds string.
fun len(s: str): int64
    ret sdslen(s)
end

# Turn the string into a smaller (or equal) string containing only the
# substring specified by the 'start' and 'end' indexes.
# 
# start and end can be negative, where -1 means the last character of the
# string, -2 the penultimate character, and so forth.
# 
# The interval is inclusive, so the start and end characters will be part
# of the resulting string.
# 
# The string is modified in-place.
# 
# Example:
# 
# s = sdsnew("Hello World");
# sdsrange(s,1,-1); => "ello World"
fun substr(s: str, start: int64, send: int64): str
    let tmp = str(s)
    sdsrange(tmp, start, send)
    ret tmp
end

# Append the specified sds 't' to the existing sds 's'.
# The problem of 'sdscatsds' is now fixed using a temporary sacrifice string
#
# From sdscatsds:
# After the call, the modified sds string is no longer valid and all the
# references must be substituted with the new pointer returned by the call.
fun concat(s: str, t: str): str
    let tmp = str(s)
    ret sdscatsds(tmp, t)
end

# Append to the sds string 's' a string obtained using printf-alike format specifier.
# The problem of 'sdscatvprintf' is now fixed using a temporary sacrifice string
#
# From sdscatvprintf:
# After the call, the modified sds string is no longer valid and all the
# references must be substituted with the new pointer returned by the call.
# 
# Example:
# 
# s = sdsnew("Sum is: ");
# s = sdscatprintf(s,"%d+%d = %d",a,b,a+b).
# 
# Often you need to create a string from scratch with the printf-alike
# format. When this is the need, just use sdsempty() as the target string:
# 
# s = sdscatprintf(sdsempty(), "... your format ...", args);
fun concat_from(s: str, fmt: int8*, ...): str
    let listx: va_list
    va_start(listx, fmt)

    let tmp = str(s)
    ret sdscatvprintf(tmp, fmt, listx)
end

# Remove the part of the string from left and from right composed just of contiguous characters found in 'cset', that is a null terminated C string.
# The problemcurr
#
# From sdstrim:
# After the call, the modified sds string is no longer valid and all the
# references must be substituted with the new pointer returned by the call.
# 
# Example:
# 
# s = sdsnew("AA...AA.a.aa.aHelloWorld :::");
# s = sdstrim(s,"Aa. :");
# printf("%s\n", s);
# 
# Output will be just "HelloWorld".
fun trim(s: str, cset: int8*): str
    let tmp = str(s)
    ret sdstrim(tmp, cset)
end

# Compare two sds strings s1 and s2 with memcmp().
# 
# Return value:
# 
# positive if s1 > s2.
# negative if s1 < s2.
# 0 if s1 and s2 are exactly the same binary string.
# 
# If two strings share exactly the same prefix, but one of the two has
# additional characters, the longer string is considered to be greater than
# the smaller one.
fun compare(s: str, s2: str): int32
    ret sdscmp(s, s2)
end

# Returns whether two sds strings are equal.
fun equals(s: str, s2: str): bool
    ret sdscmp(s, s2) == 0
end

# Apply tolower() to every character of the sds string 's'.
fun to_lower(s: str): str
    sdstolower(s)
    ret s
end

# Apply toupper() to every character of the sds string 's'.
fun to_upper(s: str): str
    sdstoupper(s)
    ret s
end

# Returns the index of the first occurence of sub in s
fun find(s: str, sub: str): int64
    let cs = c_str(s)
    let ptr = strstr(cs, c_str(sub))
    ret 0 - 1 if ptr == null else (cast("int64", ptr) - cast("int64", cs))
end

# Split 's' with separator in 'sep'. An array of sds strings is returned. *count will be set by reference to the number of tokens returned.
# 
# On out of memory, zero length string, zero length
# separator, NULL is returned.
# 
# Note that 'sep' is able to split a string using
# a multi-character separator. For example
# sdssplit("foo_-_bar","_-_"); will return two
# elements "foo" and "bar". 
fun split(cs: c_str, sep: c_str, cnt: c_int*): sds*
    let arr: sds* = sdssplitlen(cs, strlen(cs), sep, strlen(sep), cnt)
    if arr == null
        panic("Cannot split string.")
    end

    ret arr
end

# Overload; Split 's' with separator in 'sep'. An array of sds strings is returned. *count will be set by reference to the number of tokens returned.
fun split(s: str, sep: str, cnt: c_int*): sds*
    let arr: sds* = sdssplitlen(c_str(s), len(s), c_str(sep), len(sep), cnt)
    if arr == null
        panic("Cannot split string.")
    end

    ret arr
end

# Overload; Split 's' with separator in 'sep'. An array of sds strings is returned. *count will be set by reference to the number of tokens returned.
fun split(s: str, sep: c_str, cnt: c_int*): sds*
    let arr: sds* = sdssplitlen(c_str(s), len(s), sep, strlen(sep), cnt)
    if arr == null
        panic("Cannot split string.")
    end

    ret arr
end

# Join an array of C strings using the specified separator (also a C string).
# Returns the result as an sds string.
fun join(argv: void*, argc: int32, sep: int8*): str
    ret sdsjoin(argv, argc, sep)
end

# Create an sds string from a boolean value. 
fun to_str(value: bool): str
    if value
        ret str("true")
    else
        ret str("false")
    end
end

# Create an sds string from a long long value. 
# It is much faster than: sdscatprintf(sdsempty(),"%lld\n", value);
fun to_str(value: int64): str
    ret sdsfromlonglong(value)
end

# Create an sds string from a pointer value. 
fun to_str(value: void*): str
    ret str_from("%p", value)
end