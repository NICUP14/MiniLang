import stdlib.macro
import stdlib.string
import stdlib.str_list
import stdlib.str_build
import stdlib.io.print

fun str(cnt: int64, ch: int8)
    let s = empty_str.extend(cnt)
    memset(s.c_str, ch, cnt)

    ret s
end

fun concat(s: str&, ch: int8)
    ret s.concat(str(1, ch))
end

fun _format(cnt: int64, fmt: str&, ...): str
    let list: va_list
    va_start(list, fmt)

    let idx = 0
    let args_idx = 0
    let skip = false
    let pos = false
    let args = str_list(cnt, list)

    let buf = false
    let start_idx = 0
    let end_idx = 0

    let ch: int8 = 0
    let res = str_build(1000)
    while idx < fmt.len && (ch = c_str(fmt)[idx]) > '\0'
        if !skip && ch == '\\'
            skip = true
        elif !skip && ch == '{'
            if buf
                res.append(fmt.substr(start_idx, end_idx))
                buf = false
            end

            idx.incr
            pos = false
            let pos_idx = 0
            while idx < fmt.len && (
                  ch = c_str(fmt)[idx]) != '}' && isdigit(ch) > 0
                pos = true
                pos_idx = pos_idx * 10 + (ch - '0')
                idx.incr
            end

            if !pos
                pos_idx = args_idx
                args_idx.incr
            end

            if pos_idx > args.str_list_cnt || pos_idx < 0
                panicf("Invalid index: %lld\n", pos_idx)
            end
            
            res.append(args.str_list_arr[pos_idx])
        else
            if buf
                end_idx = idx
            else
                start_idx = end_idx = idx
                buf = true
            end
        end

        idx.incr
    end

    ret res.to_str
end

macro format(_fmt)
    _format(1, _fmt)
end

macro format(_fmt, _other)
    _format(count(_other), _fmt, _other)
end

fun main: int32
    let bos = 0
    alloc_start(bos)

    print(format("Hello {1} {}".str, "Hello", "Sir"))

    ret 0
end