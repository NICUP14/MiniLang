# ML standard standard definitions
alias size_t = int64
alias int = int64
alias cint = int32
alias ptr = void*
alias cstr = int8*
alias byte = int8
alias char = int8

# ML standard standard definition macros
macro null
    cast("ptr", 0)
end
macro stdin
    cast("ptr", 0)
end
macro stdout
    cast("ptr", 1)
end
macro stderr
    cast("ptr", 2)
end
macro int(_expr)
    cast("int", _expr)
end
macro ptr(_expr)
    cast("ptr", _expr)
end
macro cint(_expr)
    cast("cint", _expr)
end
macro cstr(_expr)
    cast("cstr", _expr)
end
macro byte(_expr)
    cast("byte", _expr)
end
macro char(_expr)
    cast("char", _expr)
end
macro size_t(_expr)
    cast("size_t", _expr)
end
end