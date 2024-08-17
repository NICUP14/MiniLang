import stdlib.io.print

struct range
    range_start: int64
    range_stop: int64
    range_idx: int64
end

fun start(arg: range): int64
    ret arg.range_start
end

fun stop(arg: range, idx: int64): bool
    ret idx < arg.range_stop
end

fun next(arg: range, idx: int64): int64
    ret idx + 1
end

fun main: int32
    let r = range(0, 15, 0)
    for idx in r
        println(idx)
    end
    ret 0
end