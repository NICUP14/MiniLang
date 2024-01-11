import number
import va_utils
import cstdlib

fun custom_printf(format: int8*, ...): void
    let va_list: int64[3]

    asm "stack_snapshot"
    va_start(va_list)
    va_arg(va_list)

    # DBG
    # asm "lea str_13(%rip), %rdi"
    # asm "mov %rsp, %rsi"
    # asm "xor %rax, %rax"
    # asm "call printf"

    let flag: int8 = 0
    let repeat: int8 = 0
    let arr: int8[500]
    let str: int8* = arr

    # va_arg(va_list)

    while *format != 0 
        while *format != '%' 
            strncpy(str, format, 1)
            # *str = *format 
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
            width = va_arg(va_list) 
        else: 
            let cnt = 0 
            while isdigit(*format) == 1
                cnt = cnt + 1
            end

            if cnt > 0
                width = strnToU64(format, cnt) 
            end
        end

        if *format == '%' 
            *str = '%' 
            str = str + 1
            puts("percent")
        else
            if *format == 's'
                let buf: int8* = va_arg(va_list)
                printf("string buf: %p %s\n", &buf, buf)
                strcpy(str, buf) 
                puts("string")
            else
                if *format == 'd'
                    let repr = (*format == 'd') 
                    let num: int64 = va_arg(va_list) 
                    number(str, num, flag, width) 
                    puts("signed iteger")
                else
                    if *format == 'u'
                        puts("unsigned iteger")
                        let repr = (*format == 'd') 
                        let num: int64 = va_arg(va_list) 
                        number(str, num, flag, width) 
                    end
                end
            end
        end

        format = format + 1
    end

    puts(arr)
end
end