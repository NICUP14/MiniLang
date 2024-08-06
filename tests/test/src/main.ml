import "stdlib/print"
import "stdlib/c/cstdarg"

fun var(first: int64, ...): void
    let listx: va_list
    init(listx, first)
    defer listx.deinit
    listx.get_int64.print
    listx.get_int64.print
end

fun main: int32
    var(1, 2, 3)
    ret 0
end
end
