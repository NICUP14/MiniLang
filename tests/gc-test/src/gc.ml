import "src/gc-backend"
import "stdlib/defs"

# fun start(gc: GarbageCollector*, bos: void*): void
#     gc_start(gc, bos)
# end
# 
# fun stop(gc: GarbageCollector*): void
#     gc_stop(gc)
# end

macro alloc(_lit)
    _lit = _malloc(size_of(_lit))
end

macro dealloc(_lit)
    _free(_lit), _lit = null
end