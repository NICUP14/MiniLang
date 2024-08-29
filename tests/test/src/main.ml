import stdlib.c.cstdlib
import stdlib.io.read
import stdlib.io.print

struct ex_str
    ex_cnt: int64
    ex_cs: int8*
end

macro create_ex
    ex_str(0, malloc(50))
end

fun destruct(arg: ex_str)
    # let ex_in_destr = create_ex
    free(arg.ex_cs)
end

fun test(arg: ex_str)
    let ex = create_ex
end

fun main
    test(create_ex)
    print("Hello world")
    ret 0
end