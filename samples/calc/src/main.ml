import stdlib.str_list
import stdlib.io.read
import stdlib.io.print

struct _tok_type
    err: int64
    num: int64
    add: int64
    sub: int64
    div: int64
    mult: int64
end

struct tok
    type: int64
    value: c_str
end

macro tok_type
    _tok_type(
        0, 1, 2, 3, 4, 5)
end

fun rev_tok_type_of(type: int64): str
    let cs: c_str = null
    if type == tok_type.err
        cs = "err"
    elif type == tok_type.num
        cs = "num"
    elif type == tok_type.add
        cs = "+"
    elif type == tok_type.sub
        cs = "-"
    elif type == tok_type.div
        cs = "/"
    elif type == tok_type.mult
        cs = "*"
    else
        panic("Invalid token type")
    end

    ret cs.str
end

fun _print(cs: c_stream, arg: tok&)
    let rev = rev_tok_type_of(arg.type)
    print("tok(type = ", &rev, ", value = ", arg.value, ")")
end

fun is_num(s: str&)
    for ch in s
        if isdigit(ch) == 0
            ret false
        end
    end

    ret true
end

fun tok_type_of(s: str&): int64
    if is_num(&s)
        ret tok_type.num
    elif s.equals("+")
        ret tok_type.add
    elif s.equals("-")
        ret tok_type.sub
    elif s.equals("/")
        ret tok_type.div
    elif s.equals("*")
        ret tok_type.mult
    end

    ret tok_type.err
end

fun tok(value: str&)
    ret tok(tok_type_of(&value), c_str(value))
end

fun lex(ln: str&)
    let cnt: int32 = 0
    let arr = ln.trim("\n").split(" ", &cnt)
    let list = str_list(cnt, arr)

    for it in list
        let tk = tok(&it)
        println(&tk)
    end
        
end

fun main: int32
    let bos = 0
    alloc_start(bos)

    let s = input
    lex(&s)

    ret 0
end