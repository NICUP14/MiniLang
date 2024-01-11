asm ".macro printf_rsp fmt"
asm "lea \fmt, %rdi"
asm "mov %rsp, %rsi"
asm "xor %rax, %rax"
asm "call printf"
asm ".endm"

let nassert = 1
fun assert(val: int8): void
    if val == 0
        printf("Failed assertion %lld\n", nassert)
        exit(1)
    end
    nassert = nassert + 1
end
end