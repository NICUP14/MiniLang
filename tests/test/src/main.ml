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
    let arr: int64[100]
    let arr_ptr: int64[100]* = null
    let arr_ref: int64[100]& = null
    let x = arr_ptr
    let y = arr_ref
    let test = arr
    len_of(x)
    size_of(x)

    let ex = exstruct(15, "Hello")
    let ex_ref: exstruct& = &ex
    # struct_ref(&ex)
    # let a = 15
    # let b = cast(type_of(cast("c_str", 0)), "Hello")
    # let c = decltype(a, 50)
    # println(b, ", ", c, ", ", size_of(a))
    ret 0
end