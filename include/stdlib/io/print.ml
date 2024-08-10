import stdlib.defs
import stdlib.debug
import stdlib.c.cstdlib

# Print helper functions
fun _print(st: void*, arg: bool): void
    if arg == true
        fprintf(st, "true")
    elif arg == false
        fprintf(st, "false")
    else
        panic("Logic error")
    end
end
fun _print(st: void*, arg: int8): void
    fprintf(st, "%hhd", arg)
end
fun _print(st: void*, arg: int16): void
    fprintf(st, "%hd", arg)
end
fun _print(st: void*, arg: int32): void
    fprintf(st, "%d", arg)
end
fun _print(st: void*, arg: int64): void
    fprintf(st, "%lld", arg)
end
fun _print(st: void*, arg: int8*): void
    fprintf(st, "%s", arg)
end
fun _print(st: void*, arg: void*): void
    fprintf(st, "%p", arg)
end

# Convenience macros
macro print(_arg)
    _print(stdout, _arg)
end
macro print(_arg, _other)
    print(_arg)
    print(_other)
end
macro println(_args)
    print(_args)
    puts ""
end
#! BUG: print_to redirects to bool
macro print_to(_stream, _arg)
    _print(_stream, _arg)
end
macro print_to(_stream2, _arg, _other)
    print_to(_stream2, _arg)
    print_to(_stream2, _other)
end
macro println_to(_stream3, _args)
    print_to(_stream3, _args)
    fprintf(_stream3, "\n")
end
