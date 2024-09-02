import src.lex

struct X
    x: int32
    b: range
end

fun main: int32
    let bos = 0
    alloc_start(bos)

    let s = input
    lex(s.trim(" "))

    ret 0
end