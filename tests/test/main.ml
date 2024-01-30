import "../../stdlib/cstdlib"
import "../../stdlib/stddef"
# import "../../stdlib/debug"
# import "../../stdlib/alloc"

macro to_int32(_expr)
    cast("int32", _expr)
end

fun main: int64
    let v = 15
    let r: int64& = &v
    let d = r
    let a: int32[5] = [1, 2, 3]
    ret 0
end
end