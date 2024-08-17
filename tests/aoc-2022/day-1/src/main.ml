import stdlib.io.fio
import stdlib.io.read
import stdlib.io.print
import stdlib.convert
import stdlib.alloc
import stdlib.c.cstdlib

import stdlib.string.backend

fun is_num(s: str): bool
    let idx = 0
    while idx < len(s)
        if isdigit((c_str(s))[idx]) == 0
            ret false
        end
    end

    ret true
end

# fun read_line(st: c_stream): str

fun main: int32
    let bos = 0
    gc_start(&ml_gc, &bos)

    let in_file = open_file("input.txt")
    let lines = in_file.read_file

    let idx = 0
    let cnt = 0
    let toks: sds* = sdssplitlen(c_str(lines), len(lines), "\n", 1, &cnt)

    let max_sum = 0
    let sum = 0
    while idx < cnt - 1
        let tok: str = cast("str", toks[idx])
        if is_num(tok)
            if sum > max_sum
                max_sum = sum
            end
        else
            sum = sum + to_int64(c_str(tok))
        end

        idx = idx + 1
    end

    max_sum.println

    gc_stop(&ml_gc)
    ret 0
end