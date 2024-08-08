extern fun assert(x: int8): void
extern fun strcpy(x: int64, y: int64): int64
extern fun printf(fmt: int64, ...): int64

fun main(): int64
    let fmt: int8* = "%s world"
    let arr: int8[6]
    strcpy(arr, "hello")
    printf(fmt, arr)
    ret 0
end