import "../../cstdlib"
import "../../stdlib"
import "../../va_utils"

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
    let list: int64[3]
    asm "stack_snapshot"
    va_start(&list)
    va_arg(&list)

    let ccnt = cnt
    
    let idx = 0
    let arg = 0
    let max = 0
    for(idx, 0, ccnt, (arg = va_arg(&list)), (max = cond(arg > max, arg, max)))

    ret max
end

macro max(args)
    _max(ma_cnt, args)
end

fun main: int64
    let mx = max(1, 2, 3, 4, 5)
    printf("Max: %lld", mx)

    ret 0
end
end