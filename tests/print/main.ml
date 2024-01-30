# import "everything"
import "../../stdlib/cstdlib"
import "../../stdlib/stddef"
import "../../stdlib/debug"

macro _str_has(_str, _ch)
    strchr(_str, _ch) != null
end

fun _print_arr(addr: int64*, len: int64): void
    let idx = 0
    while idx < len
        printf("%lld ", addr[idx])
        idx = idx + 1
    end
end

fun _print(addr: int64*, type: int8*, len: int64): void
    let is_ptr = _str_has(type, '*')
    let is_arr = _str_has(type, '[')

    printf("%s: ", type)
    if is_ptr
        if is_arr == false
            printf("%p", *addr)
        else
            _print_arr(addr, len)
        end
    else
        if is_arr == false
            printf("%lld", *addr)
        else
            _print_arr(addr, len)
        end
    end
end

macro print(_ident)
    _print(&_ident, type_of(_ident), len_of(_ident))
end

fun main: int64
    type_of(false)
    print(true)
    print(false)
    print(15)
    print(null)
    ret 0 
end
end