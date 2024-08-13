# string.ml - string library for ml.
# Provides a functional-like ML frontend of the sds c library.
# WARNING: Relies on the sds bindings for ML (string-backend.ml).

import stdlib.c.cstdarg
import stdlib.string.backend

alias str = sds

# Create a new sds string starting from a null terminated C string.
fun str(s: int8*): str
    ret sdsnew(s)
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
    ret sdscpy(s, t)
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
    sdsrange(s, start, send)
    ret s
end

# Append the specified sds 't' to the existing sds 's'.
# 
# After the call, the modified sds string is no longer valid and all the
# references must be substituted with the new pointer returned by the call.
fun concat(s: str, t: str): str
    ret sdscatsds(s, t)
end

# Append to the sds string 's' a string obtained using printf-alike format
# specifier.
# 
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
fun concat_printf(s: str, fmt: int8*, ...): str
    let listx: va_list
    va_start(listx, fmt)

    ret sdscatvprintf(s, fmt, listx)
end

# Remove the part of the string from left and from right composed just of
# contiguous characters found in 'cset', that is a null terminated C string.
# 
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
    ret sdstrim(s, cset)
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