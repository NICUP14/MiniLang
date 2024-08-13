import stdlib.c.cstdlib
import stdlib.c.cdef

macro add(_aptr, _aoff)
    ptr(int(_aptr) + _aoff)
end

macro sub(_sptr, _soff)
    ptr(int(_sptr) - _soff)
end

let mzf_mask: int8 = 12
let minus_flag: int8 = 8
let zero_flag: int8 = 4
let plus_flag: int8 = 2
let space_flag: int8 = 1

fun U64ToStrLen(nr: int64): int64
    let cnt = 0
    while nr > 0
        nr = nr / 10
        cnt = cnt + 1
    end

    ret cnt
end

fun U64ToStr(nr: int64, buff: int8*): int64
    let len = U64ToStrLen(nr)
    let idx = len - 1

    while nr != 0
        buff[idx] = (nr % 10) + 48
        idx = idx - 1
        nr = nr / 10
    end

    ret len
end

fun strnToU64(str: int8*, len: int64): int64
    let nr = 0
    let idx = len
    while idx < len
        nr = nr * 10 + (str[idx] - '0')
        idx = idx + 1
    end

    ret nr
end

fun number(buff: int8*, num: int64, repr: int8, flag: int8, width: int64): int64
 	let zf_set: int8  = (flag & 8)
 	let mf_set: int8  = (flag & 4)
 	let pf_set: int8  = (flag & 2)
 	let sf_set: int8  = (flag & 1)
    let sign = false
    let sign_ch = '_'
    let width_ch = '_'
    let idx = 0

  	if zf_set > 0
  	    width_ch = '0'
  	else
  	    width_ch = ' '
    end
   
    if num < 0
        sign = true
        num = 0 - num
    end
   
    if repr > 0
        if sign
            sign_ch = '-'
        else
            if sf_set > 0
                sign_ch = ' '
            elif pf_set > 0
                sign_ch = '+'
            end
        end
    end

    # puts("number before width")

    let len = U64ToStrLen(num)
    width = width - U64ToStrLen(num)
    if width < 0
        width = 0
    end

    # puts("number after width")

    if mf_set == 0
        memset(add(buff, idx), width_ch, width)
        idx = idx + width
    end

    if repr > 0
        if sf_set > 0
            buff[idx] = sign_ch
            idx = idx + 1
        else
            if pf_set > 0
                buff[idx] = sign_ch
                idx = idx + 1
            else
                if sign
                    buff[idx] = sign_ch
                    idx = idx + 1
                end
            end
        end
    end

    let nbytes = U64ToStr(num, add(buff, idx))
    idx = idx + nbytes
    # printf("DBG number: %s\n", buff)

    if mf_set > 0
        memset(add(buff, idx), width_ch, width)
        idx = idx + width
    end

    ret idx
end