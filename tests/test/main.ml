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
end

fun main(): int64
    log("Hi")

    ret 0
end
end