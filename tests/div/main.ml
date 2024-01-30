import "../../stdlib/stddef"
import "../../stdlib/cstdlib"
import "../../stdlib/debug"
import "../../stdlib/alloc"

macro pack(_args)
    _args
end

macro print3(_t1, _t2, _t3)
    _t1, _t3
    defer 1
    defer _t2
end

macro unpack(_others)
    print3(_others)
    defer 2
end

fun main: int64
    unpack(1, 2, 3)
end
end