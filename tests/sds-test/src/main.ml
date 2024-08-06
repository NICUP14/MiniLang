import "stdlib/c/cstdlib"
import "stdlib/print"
import "stdlib/string"

fun main: int32
    let mystr = str("Hello")
    let mystr2 = str_printf("Hello %s", "John Doe")
 
    ret 0
end
end
