import stdlib.io.read
import stdlib.io.print

struct ex_str
    ex_cnt: int64
    ex_cs: int8*
end

macro create_ex
    ex_str(15, malloc(50))
end

fun print_move(arg: ex_str&&): ex_str
    print(arg.ex_cnt)
    ret arg
end

fun destruct(arg: ex_str)
    let ex_in_destr = create_ex
    free(arg.ex_cs)
end

fun copy(arg: ex_str)
    ret create_ex
end

fun test(arg: ex_str)
    let ex = create_ex
end

fun main
    let x = create_ex
    move(x).ex_cnt.print
    # test(x)
    # print(strfy(create_ex))
    # print("Hello world")
    ret 0
end