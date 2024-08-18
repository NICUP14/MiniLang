import stdlib.io.print
import src.for_utils

fun main: int32
    for idx in range(10)
        println(idx)
    end
    ret 0
end