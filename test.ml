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
    let addr: int8* = buff
    let copy: int8* = addr
    while nr != 0
        *addr = nr % 10
        nr = nr / 10
        addr = addr + 1
    end

    ret addr - copy
end

fun main(): int64
    let buff: int8[3] = [0, 0, 0]
    let res: int64 = U64ToStr(64, buff)
    printf("%lld %s", res, buff)
    exit(0)
end
end