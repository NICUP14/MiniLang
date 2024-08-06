import "stdlib/c/cstdlib"

fun main(): int64
    let x: bool = true
    let c = cast("int8", x)
    let d = cast("bool*", c)
    let y = &x

    printf("Int value: %lld\n", cast("int64", x))
    if x
        printf("True")
    else
        printf("False")
    end
    ret 0
end
end