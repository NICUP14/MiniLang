extern fun assert(x: int8): void
extern fun strcpy(x: int64, y: int64): int64
extern fun printf(fmt: int64): int64

fun main(): int64
    let fmt: int8* = "%s world"
    let arr: int8[5]
    let a: int64 = 1
    let b: int64 = 2
    a = b = 3
    strcpy(arr, "hi")
    printf(fmt, arr)
    # printf("%s world", arr)
    ret 0
end
end