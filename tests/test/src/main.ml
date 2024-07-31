import "stdlib/cstdlib"
# import "stdlib/stddef"
# import "stdlib/utils"
# import "stdlib/misc"
# import "stdlib/debug"

fun _print(x: int32): void
    printf("%d\n", x)
end

fun _print(x: int64[5]*): void
    len_of(x)
    printf("arr")
end

fun _print(x: int64): void
    printf("%lld\n", x)
end

fun _print(x: int64&): void
    printf("%lld\n", x)
end

fun _print(x: bool): void
    if x
        printf("true\n")
    else:
        printf("false\n")
    end
end

macro print(arg)
    _print(arg)
end

macro print(arg, other)
    _print(arg)
    print(other)
end


fun main: int32
    let c: int64 = 5
    let d: int64[5]
    let x = d
    print(64, 65, 66, true)
    # print(&c)
    # print(true)

    # let i = 0
    # let a: int64[3] = [0, 1, 2]
    # while i < 64
    #     printf("I is now %lld\n", i)
    #     i = i + 1
    # end
    ret cast("int32", 0)
end
end
