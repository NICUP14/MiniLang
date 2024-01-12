# import printf
import cstdlib

# asm ".macro stack_snapshot"
# asm "	push %r9"
# asm "	push %r8"
# asm "	push %rcx"
# asm "	push %rdx"
# asm "	push %rsi"
# asm "	push %rdi"
# asm ".endm"
# 
# fun va_start(list: int64*): void
#     let callee_rbp: int64* = &list + 8
#     let caller_rbp: int64* = *callee_rbp
#     let caller_caller_rbp: int64* = *caller_rbp
# 
#     # list[0] (list->idx) - Current list index
#     # list[1] (list->reg_ptr) - A pointer to the stack-saved registers (caller's stack address)
#     # list[2] (list->stack_ptr) - A pointer to the stack-saved values (caller's caller stack address)
#     list[0] = 0
#     list[1] = caller_rbp + 16
#     list[2] = caller_caller_rbp + 16
# end
# 
# fun va_arg(list: int64*): int64
#     let base: int64 = 0
#     let idx: int64 = list[0]
# 
#     if list[0] <= 6
#         base = list[1]
#     else
#         base = list[2]
#         idx = idx - 6
#     end
# 
#     list[0] = list[0] + 1
#     let addr: int64* = base + idx * 8
#     ret *addr
# end
# 
# fun var(...): void
#     let va_list: int64[3]
# 
#     asm "stack_snapshot"
#     va_start(va_list)
# 
#     printf("va_list: %p\n", va_list)
#     printf("var_main_rbp: %p\n", va_list[1])
# 
#     # let arg1 = va_arg(va_list)
#     # let arg2 = va_arg(va_list)
#     # let arg3 = va_arg(va_list)
#     # printf("%lld\n", arg1)
#     # printf("%s\n", arg2)
#     # printf("%p\n", arg3)
# end

fun main(): int64
    # Stack overflow test
    let a: int8[6] = ['H', 'e', 'l', 'l', 'o', '\0']
    let v1: int8 = 0
    let v2: int8 = 0

    printf("\0%s", a)
    ret 0
end
end