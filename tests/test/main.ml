# import "everything"
import "../../stdlib/stddef"
import "../../stdlib/cstdlib"
import "../../stdlib/misc"

let gint = 0
let gptr: ptr = &gint

fun main: int64
    printf("%lld", gint)
    printf("%p", gptr)
    ret 0
end
end