import stdlib.io.read
import stdlib.io.print
import stdlib.io.file

fun test(arg: int8*): int8&
    ret arg
end

fun main
    let bos = 0
    alloc_start(bos)

    let ch: int8 = 0
    let x = test(&ch)
    
end