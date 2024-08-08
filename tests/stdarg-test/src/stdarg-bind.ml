literal("#include <stdarg.h>")
literal("#define c_va_start va_start")
literal("#define c_va_arg va_arg")

extern struct va_list
extern fun va_end(list: va_list) void
extern fun c_va_start(list: va_list, arg: void): void
extern fun c_va_arg(list: va_list, arg: void): void*

macro va_start(list, param)
    c_va_start(list, literal(param))
end

macro va_arg_voidptr(list)
    c_va_arg(list, literal("void*"))
end

macro va_arg_int64(list)
    c_va_arg(list, literal("long long"))
end

fun va_arg(list: va_list, argx: void*)
    ret c_va_arg(list, literal("void*"))
end

fun va_arg(list: va_list, argx: int64): int64
    ret cast("int64", c_va_arg(list, literal("long long")))
end