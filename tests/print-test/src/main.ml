import stdlib.c.cdef
import stdlib.io.print

struct exstruct
    cnt: int64
    cptr: void*
end

fun _print(st: c_stream, arg: exstruct): void
    print_to(st, "exstruct(cnt=", arg.cnt, ", cptr=", arg.cptr, ")")
end

fun main: int32
    exstruct(11, null).print
    ret 0
end