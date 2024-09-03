import stdlib.io.read
import stdlib.io.print
import stdlib.macro

macro max(_a2)
    _a2
end
macro max(_a, _b)
    _a if _a > _b else _b
end
macro max(_a2, _b2, _c2)
    max(max(_a2, _b2), max(_c2))
end

fun cond(maybe: bool, tval: int64, fval: int64): int64
    let val = 0 - 1
    if maybe == true
        val = tval
    else
        val = fval
    end
    ret val
end

macro form(_idx, start, stop, expr)
    while _idx < stop
        expr
        _idx = _idx + 1
    end
end

fun _max(cnt: int64, ...): int64
    let listx: va_list
    va_start(listx, cnt)

    
    let idx = 0
    let arg = 0
    let maxx = 0
    let ccnt = cnt
    form(idx, 0, ccnt,
        (arg = va_arg_int64(listx)), 
        (maxx = cond(arg > maxx, arg, maxx)))

    ret maxx
end

macro max_fun(args)
    _max(count(args), args)
end

fun main
    println max_fun(1, 2, 3, 4, 5, 6, 7, 8)
    # println max(1, 2, 3, 4, 5, 6, 7, 8)

    # let s: str& = &empty_str
    # println(delimit(" ", "Hi", "my", "name", "is", "Nicu"))
    # for i in range(10)
    #     println i
    # end
    # for i in range(10)
    #     println i
    # end
end