import "stdlib/debug"
import "stdlib/cstdlib"

# Universal copy
macro copy(_term1, _term2)
    assert(size_of _term1 == size_of _term2)
    memcpy(&_term1, &_term2, size_of _term1)
end

# Universal swap
let _swap_ptr: void* = 0
macro swap(_term1, _term2)
    assert(size_of _term1 == size_of _term2)
    _swap_ptr = malloc(size_of _term1)
    memcpy(_swap_ptr, &_term1, size_of _term1)
    memcpy(&_term1, &_term2, size_of _term1)
    memcpy(&_term2, _swap_ptr, size_of _term1)
    free(_swap_ptr)
    _swap_ptr = null
end
end