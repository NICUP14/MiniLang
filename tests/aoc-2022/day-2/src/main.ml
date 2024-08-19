import stdlib.string
import stdlib.io.file
import stdlib.io.print

fun score(ch: int8, ch2: int8): int64
    let t: int64[9] = [
        4, 1, 7, 
        8, 5, 2,
        3, 9, 6
    ]

    ret t[(ch - 'A') * 3 + (ch2 - 'X')]
end

fun part_one(st: c_stream): void
    # BUG: Invalid result (logic error)

    let sum = 0
    let cs: int8* = null

    for ln in lines(st)
        ln = ln.trim("\n")
        cs = c_str(ln)

        sum = sum + score(cs[0], cs[2])
    end

    "Part one: ".print
    sum.println
end

fun main: int32
    # GC needed for stdlib.alloc & stdlib.string
    let bos = 0
    gc_start(&ml_gc, &bos)

    # Your code here
    let in_file = open_file("input.txt")
    defer in_file.close_file()

    part_one(in_file)


    gc_stop(&ml_gc)
    ret 0
end