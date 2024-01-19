# ML standard standard definitions
typedef int = int64
typedef ptr = void*
typedef cint = int32
typedef cstr = int8*
typedef byte = int8
typedef char = int8
typedef size_t = int64

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
macro stdin
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