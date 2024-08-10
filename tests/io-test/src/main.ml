import src.io.fio
import src.io.read
import stdlib.print

fun main: int32
    # let a: bool = false
    # let b: int8 = 0
    # let c: int32 = 0
    # let d: int64 = 0

    let f = open_file("test-num.txt")

    let a = 0
    let b = 0
    let c = 0
    let d = 0
    read_from(f, a, b, c)
    print(a, " ", b) 

    # read(a, b, c, d)
    # println(a, " ", b, " ", c, " ", d)

   # let buf: int8[30]* = input("Number:", buf)
   # let _file = "test.txt"
   # let fptr = open(_file, "r")
   # if fptr == null
   #     println("Error no such file: ", _file)
   #     exit(1)
   # end

   #fptr.read.println
   #fptr.read(15).println
   # let s = input
   # s.println
   # s.len.println
end