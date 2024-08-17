import stdlib.string
import stdlib.io.print
import stdlib.alloc

macro decltype(_type, _val)
    cast(type_of(_type), _val)
end

struct exstruct
    cnt: int64
    cptr: int8*
end

fun struct_ref(arg: exstruct&): void
    _print_sep = ", "
    println(arg.cptr, arg.cnt)
end

fun main: int32
    let ex = exstruct(15, "Hello")
    let ex_ref: exstruct& = &ex
    # struct_ref(&ex)
    # let a = 15
    # let b = cast(type_of(cast("c_str", 0)), "Hello")
    # let c = decltype(a, 50)
    # println(b, ", ", c, ", ", size_of(a))
    ret 0
end