import stdlib.c.cdef
import stdlib.c.cstdlib
import stdlib.debug
import stdlib.alloc.backend

literal("#define ML_ALLOC_GC")

# Indicates whether the gc is active
let _gc_running = false

macro alloc_warn
    printf("Allocation defaults to malloc in %s:%s. Consider starting the gc by using alloc_start.\n", fun, file)
end

macro alloc_stop
    if _gc_running == false
        panic("Cannot stop an already stopped gc.")
    end

    literal("#undef s_malloc")
    literal("#undef s_realloc")
    literal("#undef s_free")
    literal("#define s_malloc malloc")
    literal("#define s_realloc realloc")
    literal("#define s_free free")

    gc_stop(&ml_gc)
    _gc_running = false
end

macro alloc_start(_lit)
    if _gc_running
        panic("Cannot start an already running gc.")
    end

    literal("#undef s_malloc")
    literal("#undef s_realloc")
    literal("#undef s_free")
    literal("#define s_malloc ml_malloc")
    literal("#define s_realloc ml_realloc")
    literal("#define s_free ml_free")

    gc_start(&ml_gc, &_lit)
    _gc_running = true
    defer alloc_stop
end

macro alloc(_lit)
    if _gc_running
        _lit = _malloc(size_of(_lit))
    else
        _lit = malloc(size_of(_lit))
        alloc_warn
    end
    if _lit == null
        panic("Allocation failed.")
    end
end

macro alloc(_lit, _size)
    if _gc_running
        _lit = _malloc(_size)
    else
        _lit = malloc(_size)
        alloc_warn
    end
    if _lit == null
        panic("Allocation failed.")
    end
end

macro alloc_zeroed(_lit)
    if _gc_running
        _lit = _calloc(1, size_of(_lit))
    else
        _lit = calloc(1, size_of(_lit))
        alloc_warn
    end
    if _lit == null
        panic("Allocation failed.")
    end
end

macro dealloc(_lit)
    if _gc_running
        _lit._free
    else
        _lit.free
    end
    _lit = cast("void*", 0)
end

macro with(_lit, _body)
    alloc(_lit)
    defer dealloc(_lit)
    _body
end