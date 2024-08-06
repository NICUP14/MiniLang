import "stdlib/c/cstdlib"
import "stdlib/defs"

alias int = int32
alias ptr = void*
alias str = int8*
alias byte = int8
alias char = int8

let nassert: int64 = 1
fun assert(val: bool): void
    if val == false
        printf("Failed assertion %lld\n", nassert)
        exit(1)
    end
    nassert = nassert + 1
end

fun main(): int32
    let arr: int64[5] = [0, 1, 2, 4, 4]
    let p: int64* = arr

    assert((p at 0) == 0)
    assert((p at 1) == 1)
    assert((p at 2) == 2)
    assert((p at 3) == 3)
    assert((p at 4) == 4)
    exit(0)
end
end