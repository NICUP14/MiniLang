import stdlib.io.fio
# import stdlib.io.read
import stdlib.io.print

fun main: int32
    let out_file = open_file("out.txt", "w")
    defer close_file(out_file)

    let a = 0
    let b: int8 = 0
    # read_from(out_file, a, b)
    # print(a, " ", b)

    println_to(out_file, "Hello World", 15)
    println_to(out_file, "Hello World at line ", 15)
    ret 0
end