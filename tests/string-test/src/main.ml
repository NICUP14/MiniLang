import stdlib.c.cstdlib
import stdlib.io.print
import stdlib.string

fun main: int32
    let mystr = str("Hello")
    mystr.concat(" World!").len.print
 
    ret 0
end
