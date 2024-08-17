import stdlib.io.read
import stdlib.io.print
import src.regex

fun main: int32
    let pattern = input().c_str
    let from = input().c_str
    let to = input().c_str
    replace(pattern, from, to).println

    # match(pattern, text).print
    # match(pattern, text).get_idx.print
    # re(pattern).search(text).print

    # let pattern = "ow"
    # let from = "Hellowgow"
    # let to = "wu"
    # match(pattern, from).found.print
end
