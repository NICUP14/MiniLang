literal("#include <stdarg.h>")
literal("#define c_va_start va_start")
literal("#define c_va_arg va_arg")

extern struct va_list
extern fun va_end(list: va_list): void
extern fun c_va_start(list: va_list, arg: int64): void
extern fun c_va_arg(list: va_list, arg: void): void*

fun destruct(arg: va_list&)
    va_end(move(arg))
end

macro va_start(_list, _param)
    # Hacky fix, literal(param) should be void
    c_va_start(move(_list), cast("int64", literal(_param)))
end

macro va_arg_voidptr(_list)
    c_va_arg(move(_list), literal("void*"))
end

macro va_arg_int64(_list)
    cast("int64", c_va_arg(move(_list), literal("long long")))
end

fun va_arg(list: va_list, argx: void*): void*
    ret c_va_arg(move(list), literal("void*"))
end

fun va_arg(list: va_list, argx: int64): int64
    ret cast("int64", c_va_arg(move(list), literal("long long")))
end

# Convenience aliases
alias get_int64 = va_arg_int64
alias get_voidptr = va_arg_voidptr