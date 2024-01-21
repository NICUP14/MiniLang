asm ".macro printf_rsp fmt"
asm "   lea \fmt, %rdi"
asm "   mov %rsp, %rsi"
asm "   xor %rax, %rax"
asm "   call printf"
asm ".endm"

# Needed for assert_exit/panic_exit
extern fun exit(status: int32): void
extern fun printf(msg: int8*, ...): int32

# Debug standard library assertion macros
macro panic_exit
    printf("Panicked in function %s, %s:%lld", fun, file, lineno)
    exit(1)
end
macro panicf(_fmt, _args)
    printf(_fmt, _args)
    printf("\n")
    panic_exit
end
macro panic(_msg)
    printf("Message: %s\n", _msg)
    panic_exit
end
macro assert_exit
    printf("Assertion failed: %s, file %s, line %lld.", line, fun, lineno)
    exit(1)
end
macro assert(_cond)
    if _cond == false
        assert_exit
    end
end
macro assert_eq(_expr, _expr2)
    if _expr != _expr2
        assert_exit
    end
end
macro assert_neq(_expr, _expr2)
    if _expr == _expr2
        assert_exit
    end
end
end