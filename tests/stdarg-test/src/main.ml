import "stdlib/cstdlib"
literal("#include <stdarg.h>")

extern struct va_list
extern fun va_start(list: va_list, arg: void): void
extern fun va_arg(list: va_list, arg: void): void*

struct c
    a: int64
end

fun arg(list: va_list, argx: int64): int64
    let val = cast("int64", va_arg(list, literal("long long")))
    ret val
end

macro start(list, param)
    va_start(list, literal(param))
end

fun var(argx: int64, ...): void
    let listx: va_list
    start(listx, argx)

    printf("%lld", arg(listx, argx))
end

fun main: int32
    let x: c
    var(1, 2)
    ret 0
end
end
