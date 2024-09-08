import stdlib.io.read
import stdlib.io.print
import stdlib.io.file

fun test(arg: int64): int8&
    ret &arg
end

fun test(arg: int8*): int8&
    ret arg
end

fun test_ptr(farg: fun(_: int8*): int8&, arg: int8*): void
    println(farg(arg))
end

# Create a sig
# let x: fun(_: int8*): int8& = ^test
# !BUG: Does not impose strict sig matching


fun main
    let bos = 0
    alloc_start(bos)

    let c: int8 = 10
    let x: fun(_: int8*): int8& = ^test
    test_ptr(^x, &c)

    ret 0
end