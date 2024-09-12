import stdlib.io.read
import stdlib.io.print

fun test[T](arg: T)
    println(type_of(arg))
end

fun testx[T, T2](arg: T, arg2: T2)
    println(type_of(arg))
    println(type_of(arg2))
end

macro apply_t(_arg)
    test(_arg)
end

macro apply_t(_arg, _other)
    apply_t(_arg)
    apply_t(_other)
end


fun main
    #! Bug
    apply_t(123, null, "15")

    test(123)
    test(null)
    test("15")
    testx(range(15), 15)

    ret 0
end