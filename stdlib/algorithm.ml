fun _max(cnt: int64, ...): int64
    let vlist: int64[3]
    asm "stack_snapshot"
    va_start(&vlist)
    va_arg(&vlist)

    let arg = 0
    let max = 0
    for(0, cnt, expr(arg = va_arg(&vlist)), expr(max = cond(arg > max, arg, max)))

    ret max
end

macro max(args)
    _max(ma_cnt, args)
end
end