# read.ml - io read library for ml.
# Extendable and safe frontend for `scanf`/`fscanf`.

import stdlib.c.cdef
import stdlib.debug
import stdlib.string
import stdlib.c.cstdlib

# Read a string from standard input until a newline is encountered.
fun input: str
    let size = 128
    let length = 0
    let ch: int32 = 1;
    let buff: int8* = malloc(size)
    defer free(buff)

    if buff == null
        panic("Unable to allocate buff");
    end

    while (ch = getchar) != '\n'
        if length + 1 >= size
            size = size * 2;
            buff = realloc(buff, size);

            if buff == null
                panic("Unable to reallocate buff");
            end
        end

        buff[length] = ch;
        length = length + 1
    end
    buff[length] = 0;

    let s = str(buff)
    ret s
end

# Read helper functions
fun _read(st: c_stream, arg: int8*): void
    fscanf(st, "%hhd", arg)
end
fun _read(st: c_stream, arg: int16*): void
    fscanf(st, "%hd", arg)
end
fun _read(st: c_stream, arg: int32*): void
    fscanf(st, "%d", arg)
end
fun _read(st: c_stream, arg: int64*): void
    fscanf(st, "%Ld", arg)
end
fun _read(st: c_stream, arg: void*): void
    panic("Cannot read void value")
end
fun _read(st: c_stream, arg: bool*): void
    panic("Cannot read boolean value")
end

# Convenience macros
macro read(_arg)
    _read(stdin, &_arg)
end
macro read(_arg, _other)
    read(_arg)
    read(_other)
end
macro read_from(_stream, _arg)
    _read(_stream, &_arg)
end
macro read_from(_stream2, _arg, _other)
    read_from(_stream2, _arg)
    read_from(_stream2, _other)
end