import src.alloc_backend
import stdlib.c.cdef

# # Starts the garbage collector
# fun start(gc: GarbageCollector*, bos: void*): void
#     gc_start(gc, bos)
# end
# 
# # Pauses the garbage collector
# fun pause(gc: GarbageCollector*): void
#     gc_pause(gc)
# end
# 
# # Resumes the garbage collector
# fun resume(gc: GarbageCollector*): void
#     gc_resume(gc)
# end
# 
# # Stops the garbage collector
# fun stop(gc: GarbageCollector*): void
#     gc_stop(gc)
# end

macro alloc(_lit)
    _lit = _malloc(size_of(_lit))
end

macro dealloc(_lit)
    _lit._free, _lit = cast("void*", 0)
end

macro with(_lit, _body)
    alloc(_lit)
    _body
end