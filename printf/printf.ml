import number
import va_utils
import cstdlib

fun custom_printf(format: int8*, ...): void
    let va_list: int64[3]

    asm "stack_snapshot"
    va_start(va_list)
    va_arg(va_list)
    # asm "stack_rewind"

    # DBG
    # asm "lea str_13(%rip), %rdi"
    # asm "mov %rsp, %rsi"
    # asm "xor %rax, %rax"
    # asm "call printf"

    # DBG
    # let arg1 = va_arg(va_list)
    # let arg2 = va_arg(va_list)
    # let arg3 = va_arg(va_list)
    # printf("arg1: %s\n", arg1)
    # printf("arg2: %s\n", arg2)
    # printf("arg3: %lld\n", arg3)

    let flag: int8 = 0
    let repeat: int8 = 0
    let arr: int8[500]
    let str: int8* = arr

    while *format != 0 
        while *format != '%' 
            printf("char: '%c'\n", *format)
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
                # puts("minus-flag")
            else
                if *format == '0' 
                    flag = flag | zero_flag 
                    # puts("zero-flag")
                else
                    if *format == '+' 
                        flag = flag | plus_flag 
                        # puts("plus-flag")
                    else
                        if *format == ' ' 
                            flag = flag | space_flag 
                            # puts("space_flag")
                        else
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
            while isdigit(*format) > 0
                cnt = cnt + 1
                format = format + 1
            end

            if cnt > 0
                width = strnToU64(format - cnt, cnt)
            end
        end

        if *format == '%' 
            *str = '%' 
            str = str + 1
            # puts("percent")
        else
            if *format == 's'
                let buf: int8* = va_arg(va_list)
                #  printf("string: %s\n", buf)
                strcpy(str, buf) 
                str = str + strlen(buf)
            else
                if *format == 'd'
                    let repr = (*format == 'd') 
                    let num: int64 = va_arg(va_list)
                    number(str, num, repr, flag, width) 
                    # puts("signed iteger")
                else
                    if *format == 'u'
                        # puts("unsigned iteger")
                        let repr = (*format == 'd') 
                        let num: int64 = va_arg(va_list) 
                        number(str, num, repr, flag, width) 
                    end
                end
            end
        end

        format = format + 1
    end

    puts(arr)
end
end