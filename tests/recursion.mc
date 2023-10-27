fun fun1(c: int64): void
    let idx: int64 = 0
    while (idx < c), idx = idx + 1
        print(idx)
        print(idx + 1)
        print(idx + 2)
    end
end

fun fun1r(c: int64): void
    if c != 0
        fun1r(c - 1)
        print(c)
    end
end

fun main(): void
    fun1r(60)
end
end