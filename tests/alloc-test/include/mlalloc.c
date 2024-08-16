#include <mlalloc.h>
#include <gc.h>

void *ml_malloc(size_t size)
{
    return gc_malloc(&ml_gc, size);
}

void *ml_calloc(size_t count, size_t size)
{
    return gc_calloc(&ml_gc, count, size);
}

void *ml_realloc(void *ptr, size_t size)
{
    return gc_realloc(&ml_gc, ptr, size);
}

void ml_free(void *ptr)
{
    return gc_free(&ml_gc, ptr);
}