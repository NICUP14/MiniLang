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

fun U64ToStr(nr: int64, buff: int8*): int64
    let len: int64 = U64ToStrLen(nr)
    let addr: int8* = buff + len - 1

    while nr != 0
        *addr = (nr % 10) + 48
        nr = nr / 10
        addr = addr - 1
    end

    ret len
end

fun main(): int64
    let buff: int8[5] = [0, 0, 0, 0, 0]
    let buffPtr: int8* = buff
    let res: int64 = U64ToStr(6969, buff)
    printf("%lld %s", res, buffPtr)
    exit(0)
end
end