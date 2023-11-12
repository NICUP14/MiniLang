extern fun printf(msg: int64, ...): int64
extern fun exit(status: int32): void

fun U64ToStrLen(nr: int64): int64
    let cnt: int64 = 0
    while nr != 0
        nr = nr / 10
        cnt = cnt + 1
    end
    ret cnt
end

fun main(): int64
    let res: int64 = U64ToStrLen(64)
    printf("%lld", res)
    exit(0)
end
end