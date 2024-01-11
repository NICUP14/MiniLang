# Minimalistic va_list implementation
# There's no way to rewind va_list (just as Stallman intended)
#
# struct va_list
# {
# 	int64_t idx;
# 	int64_t *reg_param_ptr; // Saved by caller (printf)
# 	int64_t *stack_param_ptr; // Saved by caller's caller (main)
# };

# Example usage of the va_utils module (va_utils.ml)
# fun var(...): void
#     let va_list: int64[3]
# 
#     asm "stack_snapshot"
#     va_start(va_list)
# 
#     let arg1 = va_arg(va_list)
#     let arg2 = va_arg(va_list)
#     let arg3 = va_arg(va_list)
#     
#     printf("%lld\n", arg1)
#     printf("%s\n", arg2)
#     printf("%p\n", arg3)
# end

asm ".macro stack_snapshot"
asm "	push %r9"
asm "	push %r8"
asm "	push %rcx"
asm "	push %rdx"
asm "	push %rsi"
asm "	push %rdi"
asm ".endm"

asm ".macro stack_rewind"
asm "	pop %rdi"
asm "	pop %rsi"
asm "	pop %rdx"
asm "	pop %rcx"
asm "	pop %r8"
asm "	pop %r9"
asm ".endm"

# fun _caller_stack(base_ptr: int64*): int64*
#     let callee_rbp: int64* = *(&base_ptr + 8)
#     let caller_rbp: int64* = *callee_rbp
#     ret caller_rbp
# end

fun va_start(list: int64*): void
    let callee_rbp: int64* = &list + 8
    let caller_rbp: int64* = *callee_rbp

    # list[0] (list->idx) - Current list index
    # list[1] (list->reg_ptr) - A pointer to the stack-saved registers (caller's stack address)
    # list[2] (list->stack_ptr) - A pointer to the stack-saved values (caller's caller stack address)
    list[0] = 0
    list[1] = callee_rbp + 16
    list[2] = caller_rbp + 16
end

fun va_arg(list: int64*): int64
    let base: int64 = 0
    let idx: int64 = list[0]

    if list[0] <= 6
        base = list[1]
    else
        base = list[2]
        idx = idx - 6
    end

    list[0] = list[0] + 1
    let addr: int64* = base + idx * 8
    ret *addr
end
end