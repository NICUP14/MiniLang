import "stdlib/cstdlib"
import "stdlib/stddef"
# import "stdlib/utils"
# import "stdlib/misc"
# import "stdlib/debug"

fun y: void
    1 + 2 + 3 + 4
end

fun main: int
    let c: int64 = 5
    let d: int64[5]
    let x = d
    printf("%lld", x)

    # let i = 0
    # let a: int64[3] = [0, 1, 2]
    # while i < 64
    #     printf("I is now %lld\n", i)
    #     i = i + 1
    # end
    ret 0
end
end
