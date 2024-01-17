import "../../cstdlib"
import "../../stdlib"

macro alloc_dsign(name, size)
    name = 15
    defer free(name)
end

macro with(name, val, expr)
    name = val
    expr
end

macro with_alloc2(ptr, size, expr)
    ptr = malloc(size)
    expr
    free(ptr)
end

macro with_alloc(ptr, size, expr)
    with(ptr, malloc(size), expr)
    free(ptr)
end

fun main: int64
    let c: int8* = nullptr
    with_alloc(c, 100, ((c = scanf("%s", c)), printf("%s", c)))
    ret 0
end
end