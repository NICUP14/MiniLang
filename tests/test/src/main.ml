import stdlib.io.print

struct mystr
    ptr: int8*
    length: int64
end

fun mystr(ptr: int8*)
    ret mystr(ptr, strlen(ptr))
end

fun copy(arg: mystr&)
    ret mystr(arg.ptr)
end

fun ret_by_alloc: mystr&
    let s: mystr* = null
    s.alloc

    *s = mystr("abc")
    ret s
end

fun ret_by_copy
    let s = mystr("abc")
    ret s
end

fun ret_by_move
    let s = mystr("abc")
    ret move s
end

fun main
    ret 0
end