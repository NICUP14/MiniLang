import stdlib.io.file
import stdlib.string
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

fun iter(arg: range&): range
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

# File line range
struct file_range
    file_range_st: c_stream
    file_range_str: c_str
    file_range_succ: bool
end

fun lines(arg: c_stream): file_range
    let s = empty_str
    s = extend(s, 256)

    let succ = read_line(arg, s, 256)
    ret file_range(arg, c_str(s), succ)
end

fun iter(arg: file_range&): file_range
    ret arg
end

fun next(arg: file_range&): str
    let s = empty_str
    s = extend(s, 256)

    let succ = read_line(arg.file_range_st, s, 256)
    arg.file_range_str = c_str(s)
    arg.file_range_succ = succ

    ret s
end

fun start(arg: file_range&): str
    if arg.file_range_succ == false
        panic("Attempt to read from empty file")
    end

    let s = str(arg.file_range_str)
    next(&arg)

    ret s
end

fun stop(arg: file_range&): bool
    ret arg.file_range_succ == true
end

# String range
struct c_str_range
    c_str_range_str: c_str
    c_str_range_idx: int64
    c_str_range_start: int64
    c_str_range_stop: int64
end

fun iter(arg: str&): c_str_range
    ret c_str_range(c_str(arg), 0, 0, len(arg))
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