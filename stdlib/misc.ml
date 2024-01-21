# Standard library miscelaneous functions
fun cond(maybe: bool, tval: int64, fval: int64): int64
    let val = 0
    if maybe == true
        val = tval
    else
        val = fval
    end
    ret val
end

# Standard library miscelaneous macros
macro expr(_expr)
    (_expr)
end
let _for_idx = 0
macro for(_start, _stop, _expr)
    _for_idx = _start
    while _for_idx <= _stop
        _expr
        _for_idx = _for_idx + 1
    end
end
macro for_until(_start, _stop, _expr)
    _for_idx = _start
    while _for_idx < _stop
        _expr
        _for_idx = _for_idx + 1
    end
end
macro for_idx(_idx, _start, _stop, _expr)
    _idx = _start
    while _idx <= _stop
        _expr
        _idx = _idx + 1
    end
end
macro for_idx_until(_idx, _start, _stop, _expr)
    _idx = _start
    while _idx < _stop
        _expr
        _idx = _idx + 1
    end
end
end