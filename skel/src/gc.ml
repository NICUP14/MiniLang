literal("#include <gc.h>")

extern struct GarbageCollector
let ml_gc: GarbageCollector

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

# Aliases
macro _gc_start(bos)
    gc_start(&ml_gc, &bos)
end
macro _gc_stop()
    gc_stop(&ml_gc)
end
macro _malloc(size)
    gc_malloc(&ml_gc, size)
end
macro _calloc(cnt, size)
    gc_calloc(&ml_gc, cnt, size)
end
macro _realloc(pointer, size)
    gc_realloc(&ml_gc, pointer, size)
end
macro _free(pointer)
    gc_free(&ml_gc, pointer)
end