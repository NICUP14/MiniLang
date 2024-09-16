import stdlib.convert
import stdlib.io.print
import stdlib.c.cstdlib
import stdlib.c.cstdarg
import src.number

# Not implemented in the language yet
macro break
    literal("break;")
end

# Shared range
struct shared_range
    _range: c_str_range&
end

fun iter(arg: shared_range&): shared_range&
    ret &arg
end

fun start(arg: shared_range&): int64
    arg._range.c_str_range_start = arg._range.c_str_range_idx
    ret arg._range.start
end

fun stop(arg: shared_range&): bool
    ret arg._range.stop
end

fun next(arg: shared_range&): int64
    ret arg._range.next
end

fun curr(arg: shared_range&): int8
    ret arg.start
end

fun custom_printf(format: int8*, ...): void
    let va_list: va_list
    va_start(va_list, format)

    let buf = empty_str
    let repeat = false
    let flag: int8 = 0

    let format_range = shared_range(iter(format))
    for format_ch in format_range

        for format_ch in format_range
            if format_ch == '\0' || format_ch == '%'
                break
            end

            buf = buf.concat(format_ch)
        end

        if format_ch == '\0'
            break
        end

        # Fetch next iterator
        format_range.next
        format_ch = curr(format_range)

        flag = 0
        repeat = true
        for format_ch in format_range
            if format_ch == '-' 
                flag = (flag | minus_flag)
            elif format_ch == '0'
                flag = flag | zero_flag 
            elif format_ch == '+'
                flag = flag | plus_flag 
            elif format_ch == ' '
                flag = flag | space_flag 
            else
                break
            end
        end

        let width = 0
        if format_ch == '*' 
            width = va_arg_int64(va_list) 
        else: 
            width = 0
            for format_ch in format_range
                if isdigit(format_ch) == 0
                    break
                end

                width = width * 10 + (format_ch - '0')
            end
        end
        
        if format_ch == '%' 
            buf = buf.concat(format_ch)
        elif format_ch == 's'
            let arg = c_str(va_arg_voidptr(va_list))
            buf = buf.concat(arg.str)
        elif format_ch == 'd' || format_ch == 'u'
            let repr = format_ch == 'd'
            let num: int64 = va_arg_int64(va_list) 
            buf = buf.concat(custom_printf_number(num, repr, flag, width))
        end
    end

    print(buf)
end