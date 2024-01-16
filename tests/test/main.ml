import "../../cstdlib"

namespace x
    extern fun mac(s: int8*): void
    fun printf(): int32
    end
end

namespace x
    fun fun1(): void
    end
    namespace y
        fun fun2(): void
            mac("")
            printf("")
            malloc(5)
        end
    end
end

macro print(num)
    let idx = 0
    while idx < num
        printf("%lld", idx)
        idx = idx + 1
    end
end

macro log(msg)
    printf("%s:%lld: %s", fun, lineno, msg)
    printf("")
end

fun main(): int64
    log("Hi")
    ret 0
end
end