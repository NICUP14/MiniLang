import stdlib.io.read
import stdlib.io.print
import stdlib.io.file

fun test(arg: int8*): int8&
    ret arg
end

fun main
    let bos = 0
    alloc_start(bos)

    let x = 0.0 + 5
    println(x)
    
end