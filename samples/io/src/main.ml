import stdlib.io.fio
import stdlib.io.read
import stdlib.io.print

fun main: int32
    let in_file = open_file("in.txt")
    let out_file = open_file("out.txt", "w")
    defer close_file(in_file)
    defer close_file(out_file)

    let a = 0
    let b = 0
    let c = 0
    let d = 0

    read_from(in_file, a, b, c, d)
    println("File 'out.txt' should contain: ")
    println(a, " ", b, " ", c, " ", d)
    println_to(out_file, a, " ", b, " ", c, " ", d)

    ret 0
end