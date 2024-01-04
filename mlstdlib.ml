# ML standard library functions and definitions
typedef byte = int8
typedef char = int8
typedef int = int32
typedef size_t = int64
typedef cstr = int8*

let nassert = 1
fun assert(val: int8): void
    if val == 0
        printf("Failed assertion %lld\n", nassert)
        exit(1)
    end
    nassert = nassert + 1
end
end
