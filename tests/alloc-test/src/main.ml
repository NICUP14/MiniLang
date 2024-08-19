import stdlib.c.cstdlib
import stdlib.io.print
import stdlib.c.cdef

fun test: void
    let arr: int64[3]* = null
    arr.alloc

    # Optional
    defer arr.dealloc

    arr[0] = 1
    arr[1] = 2
    arr[2] = 3
    println("Array: [", 
            arr[0], ", ", 
            arr[1], ", ", 
            arr[2], "]")
end

fun main: int32
    let bos = 0
    ml_gc_start(&bos)
    test
    ml_gc_stop

    ret 0
end