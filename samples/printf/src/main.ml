import src.number
import src.printf
# import stdlib.c.cstdlib

fun main(): int64
    let fmt = "Message: %s %+20d!"
    custom_printf(fmt, "Hello world", 16)
    ret 0
end