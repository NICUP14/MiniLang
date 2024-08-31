import stdlib.io.read
import stdlib.io.print

struct arr
    lent: int64
    xptr: int64*
end

struct arr_iter
    idx: int64
    arr_ref: arr&
end

fun iter(arg: arr&): arr_iter
    ret arr_iter(0, &arg)
end

fun start(arg: arr_iter&)
    ret arg.arr_ref.xptr at arg.idx
end

fun stop(arg: arr_iter&): bool
    ret arg.idx < arg.arr_ref.lent
end

fun next(arg: arr_iter&): int64
    arg.idx = arg.idx + 1
    ret arg.arr_ref.xptr at arg.idx
end

fun main
    let bos = 0
    alloc_start(bos)

    let ptr: int64[3]* = null
    ptr.alloc_zeroed

    ptr at 0 = 1
    ptr at 1 = 2
    ptr at 2 = 3

    let ar = arr(len_of(ptr), ptr)
    for it in ar
        println("Elem: ", it)
    end

    ret 0
end