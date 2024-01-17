# ML standard library definitions
typedef int = int32
typedef ptr = void*
typedef cstr = int8*
typedef byte = int8
typedef char = int8
typedef size_t = int64

# ML standard library macros
macro nullptr
    cast("void*", 0)
end
macro assert(cond)
    if cond == false
        printf("Assertion failed: %s, file %s, line %lld.", line, fun, lineno)
        exit(1)
    end
end
macro alloc(ident, size)
    ident = malloc(size)
    defer free(ident)
end
end