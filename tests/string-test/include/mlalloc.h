// Added by NICUP for skel/include/sdsalloc.h to interface with gc.h
#define GC_NO_GLOBAL_GC
#include <gc.h>

#ifndef ML_ALLOC_H
#define ML_ALLOC_H

extern GarbageCollector ml_gc;

void *ml_malloc(size_t size);
void *ml_calloc(size_t count, size_t size);
void *ml_realloc(void *ptr, size_t size);
void ml_free(void *ptr);

#endif