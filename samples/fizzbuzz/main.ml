import cstdlib

fun fizz_buzz(num: int64): void
    let idx = 1
    while idx <= num
        if idx % 15 == 0
            printf("%lld: FizzBuzz\n", idx)
        else
            if idx % 3 == 0
                printf("%lld: Fizz\n", idx)
            else 
                if idx % 5 == 0
                    printf("%lld: Buzz\n", idx)
                end
            end
        end

        idx = idx + 1
    end
end

fun main(): int64
    fizz_buzz(15)
    ret 0
end
end