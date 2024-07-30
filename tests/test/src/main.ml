import "stdlib/cstdlib"
# import "stdlib/stddef"
# import "stdlib/utils"
# import "stdlib/misc"
# import "stdlib/debug"

fun x: void
    1 + 2 + 3 + 4
end

fun main: int64
    let i = 0
    let a: int64[3] = [0, 1, 2]
    size_of(a)
    while i < 64
        printf("I is now %lld\n", i)
        i = i + 1
    end
    ret 0
end
end
