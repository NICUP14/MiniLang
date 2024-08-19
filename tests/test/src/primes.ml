import stdlib.io.read
import stdlib.io.print

fun is_prime(n: int64)
    if n == 2
        ret true
    end

    if n % 2 == 0
        ret false
    end

    let d = 3
    while d * d <= n
        if n % d == 0
            ret false
        end

        d = d + 2
    end

    ret true
end

fun main
    let n = 10000000
    let out_file = open_file("output.txt", "w")

    for it in range(n)
        if is_prime(it)
            println_to(out_file, it)
        end
    end

    ret 0
end