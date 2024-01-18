import "../../cstdlib"
import "../../stdlib"

macro with(name, val, expr)
    name = val
    expr
end

macro with_alloc(cptr, size, expr)
    with(cptr, malloc(size), expr)
    free(cptr)
end

macro test(name, val)
    name = val
    name at (12 + 12 + 1)
end

macro to_printf(args)
    ma_cnt
    printf(args)
end

macro assign(ident, expr)
    ident = expr
end

macro ref(ident)
    cast("int64&", &ident)
end

fun main: int64
    # let d = 0
    # let dptr: int8* = nullptr
    # assert(false)
    # test(c, nullptr)
    let x: int64* = nullptr
    to_printf(1, 2, 3, 4, 5, 6, 7, 8, 9)
    # assign(x, )
    # ident = 0
    # let c: int8* = nullptr
    # with_alloc(c, 100, (scanf("%s", c), printf("%s", c)))
    ret 0
end
end