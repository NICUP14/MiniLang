import stdlib.io.print
import src.for
import stdlib.alloc
import stdlib.string

fun main: int32
    for idx in "Hello"
        printf("%c\n", idx)
    end
    # let bos = 0
    # gc_start(&ml_gc, &bos)

    # let s1 = str("Hello")
    # let s2 = str("Hawleo")
    # let a = s1.equals("Hello".str)

    # gc_stop(&ml_gc)
    ret 0
end