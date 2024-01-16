import "../../cstdlib"

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
    lineno
    ret 0
end
end