import "../../stdlib/stddef"
import "../../stdlib/cstdlib"
import "../../stdlib/debug"
import "../../stdlib/alloc"

macro pack(_args)
    _args
end

macro print3(_t1, _t2, _t3)
    _t1 + _t3
    defer _t2
end

macro unpack_rec(_t1, _t2)
    printf(_t1)
    unpack_rec(_t2)
end

macro unpack(_others)
    unpack_rec(_others)
    # print3(_others)
end

fun main: int64
    unpack(1, 2, 3, 4)
    ret 0
end
end