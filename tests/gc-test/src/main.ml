import "stdlib/c/cstdlib"
import "stdlib/defs"
import "src/gc"

fun test: void
    let arr: int64[15]* = arr.alloc

    arr[0] = 1
    arr[1] = 2
    arr[2] = 3
    printf("0: %lld\n", arr[0])
    printf("1: %lld\n", arr[1])
    printf("2: %lld\n", arr[2])

    arr.dealloc
end

fun main: int32
    let boss = 0
    _gc_start(boss)
    test
    _gc_stop
    ret 0
end
