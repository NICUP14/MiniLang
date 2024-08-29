import src.number
import stdlib.c.cstdlib
import stdlib.c.cstdarg

fun custom_printf(format: int8*, ...): void
    let va_list: va_list
    va_start(va_list, format)

    # DBG
    # asm "lea string_13(%rip), %rdi"
    # asm "mov %rsp, %rsi"
    # asm "xor %rax, %rax"
    # asm "call printf"

    let flag: int8 = 0
    let repeat: int8 = 0
    let arr: int8[500]
    let string: int8* = arr
    let string_idx = 0
    let format_idx = 0

    while format[format_idx] != 0 
        while format[format_idx] != '%'
            # printf("char: '%c'\n", format[format_idx])
            string[string_idx] = format[format_idx]

            if format[format_idx] == 0
                puts(arr)
                ret
            end

            string_idx = string_idx + 1
            format_idx = format_idx + 1
        end

        flag = 0 
        repeat = 1
        while repeat == 1
            format_idx = format_idx + 1
            if format[format_idx] == '-' 
                flag = (flag | minus_flag)
                # puts("minus-flag")
            else
                if format[format_idx] == '0' 
                    flag = flag | zero_flag 
                    # puts("zero-flag")
                else
                    if format[format_idx] == '+' 
                        flag = flag | plus_flag 
                        # puts("plus-flag")
                    else
                        if format[format_idx] == ' ' 
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
        if format[format_idx] == '*' 
            width = va_arg_int64(va_list) 
        else: 
            let cnt = 0 
            while isdigit(format[format_idx]) > 0
                cnt = cnt + 1
                format_idx = format_idx + 1
            end

            if cnt > 0
                width = strnToU64(sub(add(format, format_idx), cnt), cnt)
            end
        end

        if format[format_idx] == '%' 
            string[string_idx] = '%' 
            string_idx = string_idx + 1
            # puts("percent")
        else
            if format[format_idx] == 's'
                let buf = c_str(va_arg_voidptr(va_list))
                # printf("stringing: %s\n", buf)
                strcpy(add(string, string_idx), buf) 
                string_idx = string_idx + strlen(buf)
            else
                if format[format_idx] == 'd'
                    let repr = cast("c_char", (format[format_idx] == 'd'))
                    let num = va_arg_int64(va_list)
                    let off = number(add(string, string_idx), num, repr, flag, width) 
                    string_idx = string_idx + off
                    # puts("signed iteger")
                else
                    if format[format_idx] == 'u'
                        # puts("unsigned iteger")
                        let repr = cast("c_char", (format[format_idx] == 'd'))
                        let num: int64 = va_arg_int64(va_list) 
                        let off = number(add(string, string_idx), num, repr, flag, width) 
                        string_idx = string_idx + off
                    end
                end
            end
        end

        format_idx = format_idx + 1
    end

    puts(arr)
end