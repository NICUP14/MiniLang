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

macro for_body(_ident)
    printf("%lld ", _ident at _for_idx)
end

macro macro_printf(t1, t2)
    macro_printf(t1)
    macro_printf(t2)
end

fun main: int64
    # let a = 15
    # let b = 30
    # let c = 0
    # let d = size_of_sum(a, b, c)
    # swap(a, b)
    # printf("a=%lld, b=%lld\n", a, b)
    let a = 5
    let a: int64[3] = [1, 2, 3]
    for(1, 5, for_body(a))
    macro_printf("Hi", "From", "Here", "Jon")
    # macro_printf("Test")
    # macro_printf("Test2", "Test2")
    ret 0
end
end