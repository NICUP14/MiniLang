import stdlib.c.cstdlib
import stdlib.c.cdef

let mzf_mask: int8 = 12
let minus_flag: int8 = 8
let zero_flag: int8 = 4
let plus_flag: int8 = 2
let space_flag: int8 = 1

macro if_set(_flag, _pos)
    (_flag & _pos) > 0
end

macro max(_arg, _arg2)
    _arg if _arg > _arg2 else _arg2
end

fun str(cnt: int64, ch: int8)
    let s = empty_str.extend(cnt)
    memset(s.c_str, ch, cnt)

    ret s
end

fun num_len(nr: int64): int64
    let cnt = 0
    while nr > 0
        nr = nr / 10
        cnt = cnt + 1
    end

    ret cnt
end

fun concat(s: str&, ch: int8)
    ret s.concat(str(1, ch))
end

fun custom_printf_number(num: int64, repr: bool, flag: int8, width: int64): str
 	let mf_set =  if_set(flag, minus_flag)
 	let zf_set  = if_set(flag, zero_flag)
 	let pf_set =  if_set(flag, plus_flag)
 	let sf_set =  if_set(flag, space_flag)

    let sign = false
    let sign_ch = '_'
    let width_ch = ('0' if zf_set else ' ')

    if num < 0
        sign = true
        num = 0 - num
    end
   
    if repr
        if sign
            sign_ch = '-'
        elif pf_set
            sign_ch = '+'
        elif sf_set
            sign_ch = ' '
        end
    end

    let buf = empty_str
    let length = num_len(num)
    width = max(width - length, 0)

    if zf_set
        buf = str(width, width_ch)
    end

    if repr && (sign || sf_set || pf_set)
        buf = buf.concat(sign_ch)
    end
    buf = buf.concat(num.to_str)

    if !zf_set
        buf = buf.concat(str(width, width_ch))
    end

    ret buf
end