import stdlib.io.print
import stdlib.c.cstdlib
import stdlib.c.cstdarg

fun var(argx: int64, ...): void
    let listx: va_list
    va_start(listx, argx)
    defer va_end(listx)

    listx.get_int64.println
end

fun main: int32
    var(1, 2)
    ret 0
end