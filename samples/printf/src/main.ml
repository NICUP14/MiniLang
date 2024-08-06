import "src/printf"
import "stdlib/c/cstdlib"

fun main(): int64
    let fmt = "Message %s 20%d!"
    custom_printf(fmt, "Hello world", 16)
    ret 0
end
end