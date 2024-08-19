import stdlib.alloc
import stdlib.io.print

fun main: int32
    # GC needed for stdlib.alloc & stdlib.string
    let bos = 0
    gc_start(&ml_gc, &bos)

    # Your code here
    println "HelloWorld"

    gc_stop(&ml_gc)
    ret 0
end