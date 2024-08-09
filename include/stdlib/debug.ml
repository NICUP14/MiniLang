import stdlib.c.cstdlib

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
    printf("Assertion failed, file %s, line %lld.", fun, lineno)
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