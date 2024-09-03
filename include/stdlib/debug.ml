# debug.ml - Debug library for ml.
# Provides customizable rust-like assertables and panic macros.

import stdlib.c.cstdlib

# Debug standard library assertion macros
macro panic_exit
    printf("Panicked in function %s, %s:%lld\n", fun, file, lineno)
    exit(1)
end
macro panicf(_fmt, _args)
    printf(_fmt, _args)
    printf("\n")
    panic_exit
end
macro panic(_msg)
    printf("%s\n", _msg)
    panic_exit
end
macro assert_exit(_cond)
    printf("Assertion '%s' failed in function %s %s:%lld.\n", strfy(_cond), fun, file, lineno)
    exit(1)
end
macro assert(_cond)
    if _cond == false
        assert_exit(_cond)
    end
end
macro assert_eq(_expr, _expr2)
    if _expr != _expr2
        assert_exit(_expr != _expr2)
    end
end
macro assert_neq(_expr, _expr2)
    if _expr == _expr2
        assert_exit(_expr == _expr2)
    end
end