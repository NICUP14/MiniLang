import "stdlib/cstdlib"
import "stdlib/stddef"

macro body(_body)
    _body
end

macro _if(_cond, _body)
    if _cond
        _body
    end
end

macro _if(_cond, _true_body, _false_body)
    if _cond
        _true_body
    else
        _false_body
    end
end

macro _defer(_expr)
    defer _expr
end

macro _main(_body)
    fun main: int64
        _body
    end
end

macro _assign(_ident, _val)
    _ident = _val
end

let a: int64* = 0
_main(
    body(a = malloc(8)),
    _defer(free(a)),
    scanf("%lld", a),

    _if(*a > 0,
        # If body
        body(
            puts("a is positive"),
            printf("Value of a is: %lld", *a)),
        # Else body
        body(
            puts("a is negative"),
            printf("Value of a is negative: %lld", *a))
    ),

    exit(0)
)
end