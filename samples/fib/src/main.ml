import "stdlib/print"

fun print_fib(num: int64): void
    let term1 = 1
    let term2 = 1
    let term3 = 0
    while term3 < num
        term1 = term2
        term2 = term3
        term3 = term1 + term2

        print(term3)
    end
end

fun main(): int64
    print_fib(100)
    ret 0
end