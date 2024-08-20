import stdlib.string
import stdlib.io.print

fun concat(s1: str, s2: str, s3: str): str
    ret s1.concat(s2).concat(s3)
end

fun main: int32
    # GC needed for stdlib.alloc & stdlib.string
    let bos = 0
    gc_start(&ml_gc, &bos)

    "Hello".str.concat(" World".str).println
    "Hello".str.concat(" World".str, "!".str).println


    gc_stop(&ml_gc)
    ret 0
end