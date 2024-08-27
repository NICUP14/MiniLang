macro repeat(_n, _body)
    for _repeat_it in range(_n)
        _body
    end
end

# Inserts a delimiter between arguments
macro delimit(_delim, _arg)
    _arg
end
macro delimit(_delim, _arg, _arg2)
    _arg, _delim, _arg2
end
macro delimit(_delim2, _arg, _arg2, _other)
    delimit(_delim2, _arg, _arg2), _delim2, delimit(_delim2, _other)
end

# Reverses the argument list
macro reverse(_arg, _arg2)
    _arg2, _arg
end
macro reverse(_arg1, _arg2, _arg3)
    reverse(_arg2, _arg3), _arg1
end

# Miscellaneous
macro not(_arg)
    false if _arg else true
end
macro neg(_arg)
    _arg = not(_arg)
end
macro incr(_arg)
    _arg = _arg + 1
end
macro decr(_arg)
    _arg = _arg - 1
end                                                  