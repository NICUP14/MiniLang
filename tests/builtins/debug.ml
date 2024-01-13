import cstdlib

asm ".macro printf_rsp fmt"
asm "   lea \fmt, %rdi"
asm "   mov %rsp, %rsi"
asm "   xor %rax, %rax"
asm "   call printf"
asm ".endm"

let nassert: int64 = 1
fun assert(val: int64): void
    if val == 0
        printf("Assertion %lld failed.", nassert)
        exit(1)
    end
    nassert = nassert + 1
end

fun assert_extra(val: int8, ln: int8*, fl: int8*, lno: int64): void
    if val == 0
        printf("Assertion %lld failed: %s, file %s, line %lld.", nassert, ln, fl, lno)
        exit(1)
    end
    nassert = nassert + 1
end
end