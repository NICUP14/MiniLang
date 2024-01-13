import "cstdlib"

let mzf_mask: int8 = 12
let minus_flag: int8 = 8
let zero_flag: int8 = 4
let plus_flag: int8 = 2
let space_flag: int8 = 1

fun U64ToStrLen(nr: int64): int64
    let cnt: int64 = 0
    while nr > 0
        nr = nr / 10
        cnt = cnt + 1
    end

    ret cnt
end

fun U64ToStr(nr: int64, buff: int8*): int64
    let len: int64 = U64ToStrLen(nr)
    let addr: int8* = buff + len - 1

    while nr != 0
        *addr = (nr % 10) + 48
        addr = addr - 1
        nr = nr / 10
    end

    ret len
end

fun strnToU64(str: int8*, len: int64): int64
    let nr: int64 = 0
    let strEnd: int8* = str + len
    while str < strEnd
        nr = nr * 10 + (*str - '0')
        str = str + 1
    end

    ret nr
end

fun number(buff: int8*, num: int64, repr: int8, flag: int8, width: int64): void
 	let zf_set: int8  = (flag & 8)
 	let mf_set: int8  = (flag & 4)
 	let pf_set: int8  = (flag & 2)
 	let sf_set: int8  = (flag & 1)
    let buff_tmp: int8* = buff
    let sign: int8 = 0
    let sign_ch = '_'
    let width_ch: int32 = '_'

  	if zf_set > 0
  	    width_ch = '0'
  	else
  	    width_ch = ' '
    end
   
    if num < 0
        sign = 1
        num = 0 - num
    end
   
    if repr > 0
        if sign == 1
            sign_ch = '-'
        else
            if sf_set > 0
                sign_ch = ' '
            end

            if pf_set > 0
                sign_ch = '+'
            end
        end
    end
   
    let len = U64ToStrLen(num)
    width = width - U64ToStrLen(num)
    if width < 0
        width = 0
    end

    if mf_set == 0
        memset(buff_tmp, width_ch, width)
        buff_tmp = buff_tmp + width
    end

    if repr > 0
        if sf_set > 0
            *buff_tmp = sign_ch
            buff_tmp = buff_tmp + 1
        else
            if pf_set > 0
                *buff_tmp = sign_ch
                buff_tmp = buff_tmp + 1
            else
                if sign == 1
                    *buff_tmp = sign_ch
                    buff_tmp = buff_tmp + 1
                end
            end
        end
    end

    buff_tmp = buff_tmp + U64ToStr(num, buff_tmp)

    if mf_set > 0
        memset(buff_tmp, width_ch, width)
        buff_tmp = buff_tmp + width
    end
end
end