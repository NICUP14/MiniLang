# import "everything"
import "../../stdlib/debug"

fun myfun: void
    panic("Help")
end

fun main: int64
    myfun
    # let c: int8* = null
    # alloc_str(c, "hello")
    ret 0
end
end