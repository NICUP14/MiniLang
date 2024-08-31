# print.ml - io print library for ml.
# Extendable and safe frontend for `printf`/`fprintf`.

import stdlib.c.cdef
import stdlib.c.cstdlib
import stdlib.debug
import stdlib.string

# Print helper functions
fun _print(st: c_stream, arg: int64): void
    fprintf(st, "%lld", arg)
end
fun _print(st: c_stream, arg: int32): void
    fprintf(st, "%d", arg)
end
fun _print(st: c_stream, arg: int16): void
    fprintf(st, "%hd", arg)
end
fun _print(st: c_stream, arg: int8): void
    fprintf(st, "%hhd", arg)
end
fun _print(st: c_stream, arg: str): void
    fprintf(st, "%s", c_str(arg))
end
fun _print(st: c_stream, arg: str&): void
    fprintf(st, "%s", c_str(arg))
end
fun _print(st: c_stream, arg: void*): void
    fprintf(st, "%p", arg)
end
fun _print(st: c_stream, arg: int8*): void
    fprintf(st, "%s", arg)
end
fun _print(st: c_stream, arg: bool): void
    if arg == true
        fprintf(st, "true")
    elif arg == false
        fprintf(st, "false")
    else
        panic("Logic error")
    end
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
