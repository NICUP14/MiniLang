# import everything
import stdlib.c.cdef
import stdlib.c.cstdlib
import stdlib.misc

# fun myfun: void
#     panic("Help")
# end

macro copy(_dest, _src)
    memcpy(&_dest, &_src, size_of(_src))
end

macro print_arr(_xident, _xarr)
    _xident = 0
    while _xident < len_of(_xarr)
        printf("Elem: %lld\n", _xarr[_xident])
        _xident = _xident + 1
    end
end

macro str_contains(_str, _ch)
    strchr(_str, _ch) != null
end

macro str_eq(_str, _str2)
    strcmp(_str, _str2) == 0
end

macro print(_expr)
    if str_eq(type_of(_expr), "bool")
        if cast("int64", _expr) == 1
            printf("Bool: true")
        else
            printf("Bool: false")
        end
    end
    if str_eq(type_of(_expr), "int64")
        printf("Integer: %lld", _expr)
    end
    if str_contains(type_of(_expr), '*')
        printf("Pointer: %p", _expr)
    end
    if str_contains(type_of(_expr), '&')
        printf("Reference: %p", _expr)
    end
    if str_contains(type_of(_expr), '[')
        printf("Arr: %p", _expr)
    end
    printf("\n")
end


fun main: int64
    # printf("%s", type_of(1 + 2 + 3))
    # let idx = 0
    # let d: int64[3]
    # copy(d, c)
    # print_arr(idx, d)

    let c: int64[3] = [1, 2, 3]
    print(true)
    print(false)
    print(&c)
    print(c)
    ret 0
end