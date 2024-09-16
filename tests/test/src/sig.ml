import stdlib.io.print

fun _count(arg: int64*): bool
    if *arg >= 3
        ret true
    else
        ret false
    end
end

fun count_if[T](f: fun(_: T): bool, arg: T, l: int64): int64
    let cnt = 0
    for itr in range(l)
        if f(&(arg[itr]))
            cnt = cnt + 1
        end
    end

    ret cnt
end

fun main
    let arr: int64[5] = [1, 2, 0, 4, 5]
    println(count_if(^_count, &arr, 5))

    ret 0
end