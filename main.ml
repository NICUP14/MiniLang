typedef int = int32
typedef cstr = int8*
extern fun exit(status: int32): void
extern fun printf(fmt: cstr, ...): int
extern fun strlen(s: cstr): int

let nassert = 1
fun assert(val: int8): void
    if val == 0
        printf("Failed assertion %lld\n", nassert)
        exit(1)
    end
    nassert = nassert + 1
end

fun main(): int64
    let idx = 0
    let str: int8* = "abcd"

    while idx < strlen(str)
        printf("%lld %c\n", idx, str at idx)
        idx = idx + 1
    end
    ret 0
end
end