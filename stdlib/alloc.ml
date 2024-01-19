# Alloc standard library functions
fun _populate(cnt: int64, ...): int64*
    let vlist: int64[3]

    asm "stack_snapshot"
    va_start(vlist)
    va_arg(vlist)

    let idx: int64 = 0
    let arr: int64* = null
    if cnt > 0
        arr = malloc(8 * cnt)
        while idx < cnt
            arr[idx] = va_arg(vlist)
            idx = idx + 1
        end
    end

    ret arr
end

# Alloc standard library macros
macro alloc_pass(_ident, _size)
    _ident = malloc(_size)
end
macro alloc_str_pass(_ident, _str)
    if _str != null
        _ident = strdup(_str)
    end
end
macro open_pass(_ident, _file, _mode)
    _ident = fopen(_file, _mode)
end
macro alloc(_ident, _size)
    alloc_pass(_ident, _size)
    defer free(_ident)
end
macro alloc_str(_iident, _sstr)
    alloc_str_pass(_iident, _sstr)
    defer free(_sstr)
end
macro open(_ident, _file, _mode)
    open_pass(_ident, _file, _mode)
    defer fclose(_ident)
end

# Alloc standard library miscelaneous macros
macro populate(_ident, _list)
    _ident = _populate(ma_cnt, _list)
    defer free(_ident)
end
macro with(_ident, _expr, _defer)
    _ident = _expr
    defer _defer
end
end