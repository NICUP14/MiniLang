extern fun printf(msg: int64, ...): int64
extern fun exit(status: int32): void

# fun U64ToStrLen(nr: int64): int64
#     let cnt: int64 = 0
#     while nr != 0
#         nr = nr / 10
#         cnt = cnt + 1
#     end
# 
#     ret cnt
# end
# 
# fun U64ToStr(nr: int64, buff: int8*): int64
#     let len: int64 = U64ToStrLen(nr)
#     let addr: int8* = buff + len - 1
# 
#     while nr != 0
#         *addr = (nr % 10) + 48
#         nr = nr / 10
#         addr = addr - 1
#     end
# 
#     ret len
# end

fun strnToU64(str: int8*, len: int64): int64
    let nr: int64 = 0
    let strEnd: int8* = str + len
    while str < strEnd
        printf("DBG: %d\n", *str - 48)
        nr = nr * 10 + (*str - 48)
        str = str + 1
    end

    ret nr
end

fun main(): int64
    let res: int64 = strnToU64("16", 2)
    printf("%d", res)
    ret 0
end
end