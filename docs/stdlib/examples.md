# Examples using the standard library

## Range-based for loop

```txt
import stdlib.io.print

fun main
    let bos = 0
    gc_start(&ml_gc, &bos)

    # for(int64_t it = 0; it < 5; it++)
    for it in range(5)
        print(it, " ")
    end

    # for(int64_t it2 = 5; it2 < 20; it2++)
    for it2 in range(5, 20)
        print("|", it2, "| ")
    end

    gc_stop(&ml_gc)
    ret 0
end
```

## Reading a file entirely

```txt
import stdlib.io.file
import stdlib.io.print

fun main
    let bos = 0
    gc_start(&ml_gc, &bos)

    let in_file = open_file("input.txt")
    defer close_file(in_file)
    println(read_file(in_file))

    gc_stop(&ml_gc)
    ret 0
end
```

## Reading a file line by line

```txt
import stdlib.string
import stdlib.io.file
import stdlib.io.print

fun main
    # GC needed for stdlib.alloc & stdlib.string
    let bos = 0
    gc_start(&ml_gc, &bos)

    let in_file = open_file("input.txt")
    defer close_file(in_file)

    for ln in lines(in_file)
        # The extracted lines contain a trailing semicolon
        ln = ln.trim("\n")
        println(ln)
    end

    gc_stop(&ml_gc)
    ret 0
end
```
