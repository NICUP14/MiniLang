import "stdlib/c/cstdlib"
import "stdlib/c/cstdarg"

fun cond(maybe: bool, tval: int64, fval: int64): int64
    let val = 0 - 1
    if maybe == true
        val = tval
    else
        val = fval
    end
    ret val
end

macro for(_idx, start, stop, expr)
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
    for(idx, 0, ccnt,
        (arg = va_arg_int64(listx)), 
        (maxx = cond(arg > maxx, arg, maxx)))

    ret maxx
end

macro max(args)
    _max(count(args), args)
end

fun main: int64
    let mx = max(1, 2, 3, 4, 5)
    printf("Max: %lld", mx)

    ret 0
end
end