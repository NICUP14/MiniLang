import stdlib.c.cdef
import stdlib.debug
import stdlib.alloc.backend

literal("#define ML_ALLOC_GC")

macro alloc(_lit)
    _lit = _malloc(size_of(_lit))
    if _lit == null
        panic("Allocation failed.")
    end
end

macro alloc_zeroed(_lit)
    _lit = _calloc(size_of(_lit))
    if _lit == null
        panic("Allocation failed.")
    end
end

macro dealloc(_lit)
    _lit._free, _lit = cast("void*", 0)
end

macro with(_lit, _body)
    alloc(_lit)
    defer dealloc(_lit)
    _body
end