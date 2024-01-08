# import printf
import cstdlib

fun main(): int64
    let num = 15
    let x = &num + 15
    printf("%p %lld\n", &num, num)
    # fun number(buff: int8*, num: int64, repr: int8, flag: int8, width: int64): void
    # let repr: int8 = 1
    # let flag: int8 = 2
    # let num = 0 - 150
    # let width = 0
    # let buff: int8[50]

    # custom_printf("%s", "Hello world")
    # number(buff, num, repr, flag, width)
    # puts(buff)

    ret 0
end
end