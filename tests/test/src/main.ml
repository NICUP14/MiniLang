import stdlib.print
import stdlib.string

fun main: int32
    let mystr = str("Hello ").concat_printf("%s (%d + %d = %d)", "You", 1, 2, 3)
    mystr.concat(str("\nIt's sunny outside")).print
    ret 0
end
