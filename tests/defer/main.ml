import "../../cstdlib"

fun void_fun(): void
    let arr: int64[5] = [0, 1, 2, 4, 4]
    let arr_size = size_of "arr"

    let ptr: int64* = malloc(arr_size)
    memcpy(ptr, arr, arr_size)
    defer free(ptr)

    let idx = 0
    while idx < len_of("arr")
        printf("%d", arr at idx)
        idx = idx + 1
    end
end

fun main(): int64
    let arr: int64[5] = [0, 1, 2, 4, 4]
    let arr_size = size_of "arr"

    let ptr: int64* = malloc(arr_size)
    memcpy(ptr, arr, arr_size)
    defer free(ptr)

    let idx = 0
    while idx < len_of("arr")
        printf("%d", arr at idx)
        idx = idx + 1
    end
    ret 0
end
end