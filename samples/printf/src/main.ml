import "src/printf"
import "stdlib/cstdlib"

fun main(): int64
    let repr: int8 = 1
    let flag: int8 = 2
    let num = 0 - 150
    let width = 0
    let buff: int8[50]


    let fmt = "Message %s %d!"
    custom_printf(fmt, "Hello world", 16)

    ret 0
end
end