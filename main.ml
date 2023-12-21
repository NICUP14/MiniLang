typedef int = int32
typedef cstr = int8*
extern fun exit(status: int): void
extern fun printf(fmt: cstr, ...): int

# let nassert: int64 = 1
# fun assert(val: int64): void
#     if val == 0
#         printf("Failed assertion %lld\n", nassert)
#         exit(1)
#     end
#     nassert = nassert + 1
# end

fun main(): int64
    let arr: int64[5] = [0, 1, 2, 3, 4]
    let c = &arr
    printf("%lld\n", (c at 3))
    ret 0
end
end