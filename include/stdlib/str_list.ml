import stdlib.string
import stdlib.c.cstdarg

macro args_to_str(_arg)
    to_str(_arg)
end
macro args_to_str(_arg, _other)
    to_str(_arg), args_to_str(_other)
end

# Stores information retuned by "str_list_start"
struct str_list
    str_list_cnt: int64
    str_list_arr: str*
end

fun _str_listv(cnt: int64, listx: va_list)
    let arr: str* = null
    alloc(arr, cnt * 8)

    let r = range(cnt)
    for it in r
        let arg: int8* = va_arg_voidptr(listx)
        arr at it = str(arg)
    end

    ret str_list(cnt, arr)
end

fun _str_list(cnt: int64, ...)
    let listx: va_list
    va_start(listx, cnt)

    ret _str_listv(cnt, move(listx))
end

fun str_list(cnt: int64, listx: va_list)
    ret _str_listv(cnt, move(listx))
end

macro str_list_from(args)
    _str_list(count(args), args_to_str(args))
end

# For-loop support
# Stores for-loop information
struct str_list_range
    str_list_range_idx: int64
    str_list_range_cnt: int64
    str_list_range_arr: str*
end

fun iter(arg: str_list&): str_list_range
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
    if stop(&arg) == true
        ret arg.str_list_range_arr at arg.str_list_range_idx
    else
        ret empty_str
    end
end