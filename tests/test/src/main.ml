import stdlib.io.fio
import stdlib.io.read
import stdlib.io.print
import stdlib.string

fun main: int32
    let a = 0
    let b: int32 = 0
    let c: int16 = 0
    let in_file = open_file("in.txt")
    let in_file2 = open_file("in2.txt")

    # read_from(in_file, a, b, c)
    # println("a, b, c = ", a, " ", b, " ", c)
    in_file2.read_file.print

    ret 0
end
