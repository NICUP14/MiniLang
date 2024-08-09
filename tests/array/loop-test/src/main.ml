import stdlib.c.cstdlib

fun main(): int64
    let idx = 0
    let arr: int32[5] = [5, 4, 3, 2, 1]

    while idx < 5
        printf("%d", arr at idx)
        idx = idx + 1
    end

    ret 0
end