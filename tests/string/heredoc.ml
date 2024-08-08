alias int = int32
alias cstr = int8*
extern fun printf(fmt: cstr, ...): int

fun main(): int64
    let my_str: cstr = <<-
        \end
        HELLO end
        HELLO WORLD
        HELLO FROM BELOW
    end
    printf("%s", my_str)
    ret 0
end