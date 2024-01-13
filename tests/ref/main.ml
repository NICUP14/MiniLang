import "cstdlib"

fun swap(term1: int64&, term2: int64&): void
    let tmp: int64 = term1
    term1 = term2
    term2 = tmp
end

fun test(ptr: int64[2]*): void
    let len = len_of("ptr")
    let size = size_of("ptr")
    let size_ch = cast("int8", size + 1)
    let ch = 'c'
    let widen = cast("int64", ch)
    let unwiden = cast("int8*", 15)
end

fun main(): int64
    let term1 = 15
    let term2 = 30
    let ptr: int64[5]* = &term1
    let arr: int8[5] = [1, 2, 3, 4, 5]
    swap(&term1, &term2)
    printf("Terms: %lld %lld", term1, term2)
    ret 0
end
end