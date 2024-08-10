import stdlib.c.cstdlib
import src.cstdarg

fun var(argx: int64, ...): void
    let listx: va_list
    ml_va_start(listx, argx)

    printf("%lld", ml_va_arg(listx, argx))
end

fun main: int32
    let x: c
    var(1, 2)
    ret 0
end