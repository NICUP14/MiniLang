import "../../cstdlib"
import "../../stdlib"

macro with(name, val, expr)
    name = val
    expr
end

macro with_alloc(ptr, size, expr)
    with(ptr, malloc(size), expr)
    free(ptr)
end

macro test(name, val)
    name = val
    name at (12 + 12 + 1)
end

fun main: int64
    let d = 0
    let c: int8* = nullptr
    assert(false)
    test(c, nullptr)
    with_alloc(c, 100, (scanf("%s", c), printf("%s", c)))
    ret 0
end
end