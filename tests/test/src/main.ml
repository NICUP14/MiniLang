import stdlib.io.read
import stdlib.io.print
import stdlib.io.file

fun main
    let bos = 0
    alloc_start(bos)

    let arr: int64[3]* = null
    arr.alloc_zeroed

    # arr at 0 = 1
    # arr at 1 = 32
    # arr at 2 = 4

    for i in range(3)
        println(arr at i)
    end
end