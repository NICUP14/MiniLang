import "stdlib/cstdlib"
# import "stdlib/stddef"
# import "stdlib/utils"
# import "stdlib/misc"
# import "stdlib/debug"

# extern fun va_start(list: void, arg: void): void*
# extern fun va_arg(list: void, arg: void): void*
# 
# macro _va_start(list, param)
#     va_start(literal("(va_list)", list), literal(param))
# end
# 
# fun _va_arg(list: void*, arg: int64): int64
#     let val = cast("int64", va_arg(literal("(va_list)", list), literal("long long")))
#     ret val
# end
# 
# fun var(arg: int64, ...): void
#     let listx: int64[10]
#     _va_start(listx, arg)
# 
#     printf("%lld", _va_arg(listx, arg))
# end

extern struct mystr3

struct mystr
    a: int64
    b: int64
    c: int64
end

struct mystr2
    d: int64
end

fun printstr(arg: mystr): void
    printf("%lld", arg.a)
end

fun main: int32
    let x: mystr
    let c: mystr = x

    
    ret 0
end
end
