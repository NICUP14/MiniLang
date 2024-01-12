import printf
import cstdlib

fun main(): int64
    # fun number(buff: int8*, num: int64, repr: int8, flag: int8, width: int64): void
    let repr: int8 = 1
    let flag: int8 = 2
    let num = 0 - 150
    let width = 0
    let buff: int8[50]

    # asm "lea str_13(%rip), %rdi"
    # asm "mov %rsp, %rsi"
    # asm "xor %rax, %rax"
    # asm "call printf"

    custom_printf("Message: %s %+d", "Hello world", 16)

    ret 0
end
end