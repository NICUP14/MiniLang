import stdlib.c.cdef
import stdlib.c.cstdlib

# Integer range
struct range
    range_idx: int64
    range_start: int64
    range_stop: int64
end

fun range(range_start: int64, range_stop: int64): range
    ret range(0, range_start, range_stop)
end

fun range(range_stop: int64): range
    ret range(0, 0, range_stop)
end

fun iter(arg: range): range
    ret arg
end

fun start(arg: range&): int64
    ret arg.range_start
end

fun stop(arg: range&): bool
    ret arg.range_idx < arg.range_stop
end

fun next(arg: range&): int64
    arg.range_idx = arg.range_idx + 1
    ret arg.range_idx
end

# String range
struct c_str_range
    c_str_range_str: c_str
    c_str_range_idx: int64
    c_str_range_start: int64
    c_str_range_stop: int64
end

fun iter(arg: c_str): c_str_range
    ret c_str_range(arg, 0, 0, strlen(arg))
end

fun start(arg: c_str_range&): c_char
    ret (arg.c_str_range_str) at (arg.c_str_range_start)
end

fun stop(arg: c_str_range&): bool
    ret arg.c_str_range_idx < arg.c_str_range_stop
end

fun next(arg: c_str_range&): c_char
    arg.c_str_range_idx = arg.c_str_range_idx + 1
    ret arg.c_str_range_str at arg.c_str_range_idx
end