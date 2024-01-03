typedef int = int32
typedef cstr = int8*
extern fun exit(status: int32): void
extern fun printf(fmt: cstr, ...): int
extern fun strlen(s: cstr): int

# let nassert = 1
# fun assert(val: int8): void
#     if val == 0
#         printf("Failed assertion %lld\n", nassert)
#         exit(1)
#     end
#     nassert = nassert + 1
# end

fun main(): int64
    let idx = 0
    let arr: int32[5] = [5, 4, 3, 2, 1]

    while idx < 5
        printf("%d", arr at idx)
        idx = idx + 1
    end

    ret 0
end
end