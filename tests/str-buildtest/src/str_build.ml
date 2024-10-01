import stdlib.c.cstdlib
import stdlib.string

struct str_build
    str_build_len: int64
    str_build_size: int64
    str_build_cs: c_str
end

fun str_build(size:  int64)
    let cs = alloc_size(size, true)
    ret str_build(0, size, cs)
end

fun len(sb: str_build&)
    ret sb.str_build_len
end

fun capacity(sb: str_build&)
    ret sb.str_build_size
end

fun to_str(sb: str_build&)
    ret str(sb.str_build_cs)
end

fun to_cstr(sb: str_build&)
    let dupl = alloc_size(sb.len)
    let src = sb.str_build_cs
    memcpy(src, dupl, sb.str_build_len)

    ret dupl
end

fun append(sb: str_build&, ch: int8)
    if sb.len == sb.capacity
        panicf("Attempt to append character %c to max-capacity str_build\n", ch)
    end

    sb.str_build_cs[sb.str_build_len] = ch
    sb.str_build_len = sb.str_build_len + 1

    ret sb
end

fun append(sb: str_build&, cs: int8*)
    let cs_len = strlen(cs)
    if sb.len + cs_len == sb.capacity
        panicf("Attempt to append c string '%s' to max-capacity str_build\n", cs)
    end
    
    for it in range(cs_len)
        sb.append(cs[it])
    end

    ret sb
end

fun append(sb: str_build&, s: str&)
    let s_len = s.len
    if sb.len + s_len == sb.capacity
        panicf("Attempt to append string '%s' to max-capacity str_build\n", c_str(s))
    end

    ret sb.append(c_str(s))
end