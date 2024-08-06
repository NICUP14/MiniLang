# Minimalistic va_list implementation
# WARNING: Works correctly only for assembly
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
#     asm "stack_rewind"
# 
#     let arg1 = va_arg(va_list)
#     let arg2 = va_arg(va_list)
#     let arg3 = va_arg(va_list)
#     
#     printf("%lld\n", arg1)
#     printf("%s\n", arg2)
#     printf("%p\n", arg3)
#     va_end(va_list)
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

# va_list type definition (int64[3]*)
alias va_list = int64*

fun _va_start(list: va_list): va_list
    let callee = cast("int64", &list) + 8
    let callee_rbp = cast("int64*", callee)
    let caller_rbp = cast("int64*", *callee_rbp)

    # 24 = return_addr (from call) + rbp (from calle) + 8 (starting ML offset)
    let reg_ptr: int64* = cast("int64*", cast("int64", callee_rbp) + 24)
    let stack_ptr: int64* = cast("int64*", cast("int64", caller_rbp) +  24)

    let addr: int64* = malloc(48)
    memcpy(addr, reg_ptr, 48)

    # list[0] (list->idx) - Current list index
    # list[1] (list->reg_ptr) - A pointer to the stack-saved registers (caller's stack address)
    # list[2] (list->stack_ptr) - A pointer to the stack-saved values (caller's caller stack address)
    list[0] = 0
    list[1] = cast("int64", addr)
    list[2] = cast("int64", stack_ptr)

    ret list
end

fun _va_end(list: va_list): void
    free(cast("void*", cast("int64", list) + 8))
end

macro va_start(list)
    _va_start(list)
    defer _va_end(list)
end

fun va_arg(list: va_list): int64
    let base: int64 = 0
    let idx: int64 = list[0]

    if list[0] <= 6
        base = list[1]
    else
        base = list[2]
        idx = idx - 6
    end

    list[0] = list[0] + 1
    let addr = cast("int64*", base + idx * 8)
    ret *addr
end
end