import stdlib.io.read
import stdlib.io.print

fun test[T](arg: T)
    println(type_of(arg))
end

fun main
    #test(123)
    test(null)
    test("15")

    ret 0
end