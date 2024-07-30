import "stdlib/stddef"
import "stdlib/cstdlib"
import "stdlib/debug"
import "stdlib/alloc"

extern fun print(param: int64): void

macro pack(_args)
    _args
end

macro print3(_t1, _t2, _t3)
    _t1 + _t3
    defer _t2
end

macro unpack_rec(_t1)
    print(_t1)
end

macro unpack_rec(_t1, _t2)
    print(_t1)
    unpack_rec(_t2)
end

macro unpack(_others)
    unpack_rec(_others)
end

fun main
: int64
    let i = 15
    ret 0
end
end