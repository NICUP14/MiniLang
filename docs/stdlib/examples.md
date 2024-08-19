# Examples using the standard library

## Reading a file line by line

```txt
import stdlib.string
import stdlib.io.fio
import stdlib.io.print

fun main: int32
    # GC needed for stdlib.alloc & stdlib.string
    let bos = 0
    gc_start(&ml_gc, &bos)

    let in_file = open_file("input.txt")
    for ln in lines(in_file)
        # The extracted lines contain a trailing semicolon
        ln = ln.trim("\n")
        println(ln)
    end

    gc_stop(&ml_gc)
    ret 0
end
```
