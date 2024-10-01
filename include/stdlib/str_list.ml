import stdlib.macro
import stdlib.debug
import stdlib.string
import stdlib.c.cstdarg

macro args_to_str(_arg)
    to_str(_arg)
end

# Converts each argument of he list to string
macro args_to_str(_arg, _other)
    to_str(_arg), args_to_str(_other)
end

# Stores an array of strings
struct str_list
    str_list_size: int64
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

    ret str_list(cnt, cnt, arr)
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
    _str_list(count(args), count(args), args_to_str(args))
end

fun len(list: str_list&)
    ret list.str_list_cnt
end

fun capacity(list: str_list&)
    ret list.str_list_size
end

fun append(list: str_list&, arg: c_str)
    if list.len == list.capacity
        panicf("Attempt to append c string '%s' to max-capacity str_list\n", arg)
    end

    list.str_list_arr[list.str_list_cnt] = arg.str
    list.str_list_cnt.incr

    ret list
end

fun append(list: str_list&, arg: str&)
    if list.len == list.capacity
        panicf("Attempt to append string '%s' to max-capacity str_build\n", c_str(arg))
    end
    
    ret list.append(c_str(arg))
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