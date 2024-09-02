import stdlib.io.read
import stdlib.io.print
import stdlib.macro

fun main
    let bos = 0
    alloc_start(bos)

    let a = input
    let b = str(a.str)
    println a

    # let s: str& = &empty_str
    # println(delimit(" ", "Hi", "my", "name", "is", "Nicu"))
    # for i in range(10)
    #     println i
    # end
    # for i in range(10)
    #     println i
    # end
end