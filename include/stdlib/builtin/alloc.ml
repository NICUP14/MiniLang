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

fun alloc_size(sz: int64, fill: bool): void*
    let ptr = null
    if _gc_running
        ptr = _malloc(sz)
    else
        ptr = malloc(sz)
        alloc_warn
    end

    if ptr == null
        panic("Allocation failed.")
    end

    if fill
        memset(ptr, 0, 1)
    end

    ret ptr
end

fun alloc_size(size: int64): void*
    ret alloc_size(size, false)
end

macro alloc(_lit)
    _lit = alloc_size(size_of(_lit))
end

macro alloc(_lit, _size)
    _lit = alloc_size(_size)
end

macro alloc_zeroed(_lit)
    _lit = alloc_size(size_of(_lit), true)
end

macro alloc_zeroed(_lit, _size)
    _lit = alloc_size(_size, true)
end

macro dealloc(_lit)
    if _gc_running
        _lit._free
    else
        _lit.free
    end
    _lit = null
end

macro with(_lit, _body)
    alloc(_lit)
    defer dealloc(_lit)
    _body
end