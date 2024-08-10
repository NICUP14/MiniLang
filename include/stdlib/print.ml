import stdlib.c.cstdlib

# Print helper functions
fun _print(arg: bool): void
    if arg == true
        printf("true")
    else
        printf("false")
    end
end
fun _print(arg: int8): void
    printf("%hhd", arg)
end
fun _print(arg: int16): void
    printf("%hd", arg)
end
fun _print(arg: int32): void
    printf("%d", arg)
end
fun _print(arg: int64): void
    printf("%lld", arg)
end
fun _print(arg: int8*): void
    printf("%s", arg)
end
fun _print(arg: void*): void
    printf("%p", arg)
end

# Convenience macros
macro print(_arg)
    _print(_arg)
end
macro print(_arg, _other)
    print(_arg)
    print(_other)
end
macro println(_args)
    print(_args)
    puts ""
end