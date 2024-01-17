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