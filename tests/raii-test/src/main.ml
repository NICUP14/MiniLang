import stdlib.macro
import stdlib.io.print

struct test
    op1: int64
    op2: int64
end

fun test(op1: int64)
    println("Constructor")
    ret test(op1, 0)
end

fun copy(arg: test&)
    println("Copy")
    ret test(arg.op1, arg.op2)
end

fun destruct(arg: test&)
    println("Destruct")
end

fun ret_test
    ret test(0)
end

fun main
    let a = ret_test
    a = ret_test
    ret 0
end