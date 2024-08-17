literal("#define GC_NO_GLOBAL_GC")
literal("#include <gc.h>")
literal("#include <mlalloc.h>")

extern struct GarbageCollector
let ml_gc: GarbageCollector

# Ml allocator functions (mlalloc.h)
extern fun ml_malloc(size: int64): void*
extern fun ml_calloc(cnt: int64, size: int64): void*
extern fun ml_realloc(ptr: void*, size: int64): void*
extern fun ml_free(ptr: void*): void

# Starting, stopping, pausing, resuming and running the GC.
extern fun gc_start(gc: GarbageCollector*, bos: void*): void
extern fun gc_stop(gc: GarbageCollector*): int64
extern fun gc_pause(gc: GarbageCollector*): void
extern fun gc_resume(gc: GarbageCollector*): void
extern fun gc_run(gc: GarbageCollector*): int64

# Allocating and deallocating memory.
extern fun gc_malloc(gc: GarbageCollector*, size: int64): void*
extern fun gc_calloc(gc: GarbageCollector*, cnt: int64, size: int64): void*
extern fun gc_realloc(gc: GarbageCollector*, pointer: void*, size: int64): void*
extern fun gc_free(gc: GarbageCollector*, pointer: void*): void*

# Convenience macros
# fun ml_gc_start(bos: void*): void
#     gc_start(&ml_gc, bos)
# end
# fun ml_gc_stop: void
#     gc_stop(&ml_gc)
# end
macro _malloc(size)
    ml_malloc(size)
end
macro _calloc(cnt, size)
    ml_calloc(cnt, size)
end
macro _realloc(pointer, size)
    ml_realloc(pointer, size)
end
macro _free(pointer)
    ml_free(pointer)
end