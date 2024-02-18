# Alloc standard library macros
let _alloc_cnt = 0
let _alloc_fcnt = 0
macro _alloc_assert
    if _alloc_cnt != 0
        panicf("Memory leak due to alloc_pass/alloc_str_pass, count: %lld", _alloc_cnt)
    end
    if _alloc_fcnt != 0
        panicf("Memory leak due to open_pass, count: %lld", _alloc_fcnt)
    end
end
macro alloc_assert
    defer _alloc_assert
end
macro alloc_dealloc(_ident)
    free(_ident)
    _alloc_cnt = _alloc_cnt - 1
end
macro alloc_close(_ident)
    fclose(_ident)
    _alloc_fcnt = _alloc_fcnt - 1
end
macro alloc_pass(_ident, _size)
    _ident = malloc(_size)
    _alloc_cnt = _alloc_cnt + 1
end
macro alloc_str_pass(_ident, _str)
    if _str != null
        _ident = strdup(_str)
        _alloc_cnt = _alloc_cnt + 1
    end
end
macro alloc_open_pass(_ident, _file, _mode)
    _ident = fopen(_file, _mode)
    _alloc_fcnt = _alloc_fcnt + 1
end
macro alloc(_aident, _size)
    alloc_pass(_aident, _size)
    defer alloc_dealloc(_aident)
end
macro alloc_str(_sident, _str)
    alloc_str_pass(_sident, _str)
    defer alloc_dealloc(_sident)
end
macro alloc_open(_fident, _file, _mode)
    alloc_open_pass(_fident, _file, _mode)
    defer alloc_close(_fident)
end

# Alloc standard library miscelaneous macros
macro with(_ident, _expr, _defer)
    _ident = _expr
    defer _defer
end
end