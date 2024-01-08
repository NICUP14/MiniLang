import number
import cstdlib

extern fun _va_start(list: void*): void
extern fun _va_arg(list: void*): int64

fun va_start(list: int64*): void
    let callee_rbp: int64* = &list - 8
    let caller_rbp: int64* = *callee_rbp
end

# fun va_arg(list: int64*): int64
# end

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
                puts("minus-flag")
            else
                if *format == '0' 
                    flag = flag | zero_flag 
                    puts("zero-flag")
                else
                    if *format == '+' 
                        flag = flag | plus_flag 
                        puts("plus-flag")
                    else
                        if *format == ' ' 
                            flag = flag | space_flag 
                            puts("space_flag")
                        else
                            puts("repeat == 0")
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
            while isdigit(*format) == 1
                cnt = cnt + 1
            end

            let num = 0
            width = strnToU64(*format, &num, cnt) 
        end

        puts("specifier processing")
            
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