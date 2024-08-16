alias int = int32
alias c_str = int8*
extern fun printf(fmt: c_str, ...): int

fun main(): int64
    let my_str: c_str = <<-
        \end
        HELLO end
        HELLO WORLD
        HELLO FROM BELOW
    end
    printf("%s", my_str)
    ret 0
end