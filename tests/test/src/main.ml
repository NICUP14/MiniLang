import stdlib.c.cdef
import stdlib.string
import stdlib.io.print
import src.str_list

# va_str => Convert variadic args to str* array
# args => str(arg1), str(arg2), str(arg3)

fun main
    warn("WTF bro", "124", "235")

    defer println "HI"
    let bos = 0
    alloc_start(bos)

    let arg = str_list_from(1, 2, 3, 4, true)
    for it in arg
        println(it)
    end
end