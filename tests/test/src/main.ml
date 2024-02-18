import "stdlib/cstdlib"
import "stdlib/stddef"
import "stdlib/utils"
import "stdlib/misc"
import "stdlib/debug"

macro size_of_sum(_arg)
    size_of(_arg)
end

macro size_of_sum(_arg, _args)
    size_of(_arg) + size_of_sum(_args)
end

macro macro_printf(t)
    printf("%s ", t)
end

macro for_body(_ident, _idx)
    printf("%lld ", _ident at _idx)
end

macro for_body(_ident, _idx)
    printf("%lld ", _ident at _idx)
end

macro macro_printf(t1, t2)
    macro_printf(t1)
    macro_printf(t2)
end

macro _reverse(_t1, _t2)
    _t2, _t1
end

macro reverse(_t)
    _t
end

macro reverse(_t1, _t2)
    _reverse(_t1, reverse(_t2))
end

fun main: int64
    let i = 0
    let arr: int64[3] = [1, 2, 3]
    # let a = x
    # let a = 15
    # let b = 30
    # let c = 0
    # let d = size_of_sum(a, b, c)
    # swap(a, b)
    # printf("a=%lld, b=%lld\n", a, b)

    let b: int64[3] = [1, 2, 3]
    for(1, 5,
        printf("%lld", arr at _for_idx)
    )

    macro_printf(
        "Hi", 
        "From", 
        "Here", 
        "Jon"
    )
    # macro_printf("Test")
    # macro_printf("Test2", "Test2")
    ret 0
end
end