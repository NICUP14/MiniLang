import stdlib.string
import stdlib.c.cstdarg

macro _va_str_map(_arg)
    to_str(_arg)
end
macro _va_str_map(_arg, _other)
    to_str(_arg), _va_str_map(_other)
end

# Stores information retuned by "str_list_start"
struct str_list
    str_list_cnt: int64
    str_list_arr: str*
end

fun _str_list(cnt: int64, ...)
    let arr: str* = null
    alloc(arr, cnt * 8)

    let listx: va_list
    va_start(listx, cnt)

    for it in range(cnt)
        let arg: int8* = va_arg_voidptr(listx)
        arr at it = str(arg)
    end

    ret str_list(cnt, arr)
end

macro str_list_from(args)
    _str_list(count(args), _va_str_map(args))
end

# For-loop support
# Stores for-loop information
struct str_list_range
    str_list_range_idx: int64
    str_list_range_cnt: int64
    str_list_range_arr: str*
end

fun iter(arg: str_list): str_list_range
    ret str_list_range(0, arg.str_list_cnt, arg.str_list_arr)
end

fun start(arg: str_list_range&)
    ret arg.str_list_range_arr at arg.str_list_range_idx
end

fun stop(arg: str_list_range&)
    ret arg.str_list_range_idx < arg.str_list_range_cnt
end

fun next(arg: str_list_range&)
    arg.str_list_range_idx = arg.str_list_range_idx + 1
    ret arg.str_list_range_arr at arg.str_list_range_idx
end