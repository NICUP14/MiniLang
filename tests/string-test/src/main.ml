import stdlib.string
import stdlib.io.file
import stdlib.io.print
import stdlib.convert
import stdlib.c.cstdlib
import src.for

fun part_one(st: c_stream): void
    let sum = 0
    let max_sum = 0
    let s: str = extend(empty_str, 256)

    while read_line(st, s, 256)
        s = s.trim("\n")

        if s.len == 0
            max_sum = sum if sum > max_sum else max_sum
            sum = 0
        else
            sum = sum + to_int64(c_str(s))
        end
    end

    "Part one: ".print
    max_sum.println
end

fun part_two(st: c_stream): void
    let sum = 0
    let max_sum = 0
    let max_sum2 = 0
    let max_sum3 = 0
    let s: str = extend(empty_str, 256)

    while read_line(st, s, 256)
        s = s.trim("\n")

        if s.len == 0
            if sum > max_sum
                max_sum3 = max_sum2
                max_sum2 = max_sum
                max_sum = sum

            elif sum > max_sum2
                max_sum3 = max_sum2
                max_sum2 = sum

            elif sum > max_sum3
                max_sum3 = sum
            end

            sum = 0
        else
            sum = sum + to_int64(c_str(s))
        end
    end

    "Part two: ".print
    (max_sum + max_sum2 + max_sum3).println
end


fun main: int32
    let bos = 0
    gc_start(&ml_gc, &bos)

    let in_file = open_file("input.txt")
    part_one(in_file)
    rewind(in_file)
    part_two(in_file)

    gc_stop(&ml_gc)
    ret 0
end