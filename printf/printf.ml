#  Roughly equivalent pseudocode 
# while *format != NULL: 
#     while *format != '%': 
#         *str++ = *format++ 
# 
#     flag = 0 
#     repeat: 
#     format++ 
#     if *format == '-': 
#         flag |= minus_flag 
#         goto repeat 
#     if *format == '0': 
#         flag |= zero_flag 
#         goto repeat 
#     if *format == '+': 
#         flag |= plus_flag 
#         goto repeat 
#     if *format == ' ': 
#         flag |= space_flag 
#         goto repeat 
#         
#     if *format == '*': 
#         width=get_next_arg(uint64) 
#     else: 
#         cnt = 0 
#         while isdigit(*format) 
#             cnt++ 
#         width = str_to_uint64(*format, num, cnt) 
#         
#     if *format == '%': 
#         *str++ = '%' 
#         
#     if *format == 's': 
#         strcpy(str, buf) 
#         
#     if *format == 'd' || *format == 'u': 
#         repr = (*format == 'd') 
#         num = get_next_arg(uint64) 
#         number(buf, num, ...) 

import number
import cstdlib

extern fun _va_start(list: void*): void
extern fun _va_arg(list: void*): int64

fun custom_printf(format: int8*, ...): void
    let flag: int8 = 0
    let repeat: int8 = 0
    let arr: int8[500]
    let str: int8* = arr

    let va_list: int64[3]
    _va_start(va_list)

    while *format != 0 
        while *format != '%' 
            *str = *format 
            format = format + 1
            str = str + 1
        end

        flag = 0 
        repeat = 1
        while repeat == 1
            format = format + 1
            if *format == '-' 
                flag = flag | minus_flag 
            else
                if *format == '0' 
                    flag = flag | zero_flag 
                else
                    if *format == '+' 
                        flag = flag | plus_flag 
                    else
                        if *format == ' ' 
                            flag = flag | space_flag 
                        else
                            repeat = 0
                        end
                    end
                end
            end
        end
        
        let width = 0
        if *format == '*' 
            width = _va_arg(va_list) 
        else: 
            let cnt = 0 
            while isdigit(*format) 
                cnt = cnt + 1
            end

            let num = 0
            width = strnToU64(*format, &num, cnt) 
        end
            
        if *format == '%' 
            *str = '%' 
            str = str + 1
        end
            
        if *format == 's'
            let buf: int8* = _va_arg(va_list)
            strcpy(str, buf) 
        end
            
        if *format == 'd'
            let repr = (*format == 'd') 
            let num: int64 = _va_arg(va_list) 
            number(buf, num, flag, width) 
        else
            if *format == 'u'
                let repr = (*format == 'd') 
                let num: int64 = _va_arg(va_list) 
                number(buf, num, flag, width) 
            end
        end
    end
end
end