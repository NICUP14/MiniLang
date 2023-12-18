extern fun printf(fmt: int64, ...): int64
extern fun exit(status: int32): void

typedef uint = int64
typedef ptr = int64*

let nassert: int64 = 1
fun assert(val: int64): void
    if val == 0
        printf("Failed assertion %lld\n", nassert)
        exit(1)
    end
    nassert = nassert + 1
end

fun main(): uint
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