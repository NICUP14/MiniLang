import "stdlib/print"
import "stdlib/string"

fun main: int32
    # Is equivalent to:
    # print(concat(str("Hello "), str("World!")))
    (str("Hello ").
        concat(str("World!")).
        print)
end