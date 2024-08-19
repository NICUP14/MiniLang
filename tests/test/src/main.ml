import stdlib.builtin.*
import stdlib.string

fun maybe(x: int64, y: int64)
    if x == 5
        ret 1 + 2
    else
        ret "15"
    end
end

fun main
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