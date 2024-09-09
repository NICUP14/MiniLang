import stdlib.io.print

# fun test(arg: int64): int8&
#     ret &arg
# end
# 
# fun test(arg: int8*): int8&
#     ret arg
# end
# 
# fun test_ptr(farg: fun(_: int8*): int8&, arg: int8*): void
#     println(farg(arg))
# end

fun main
    let i = 0
    while i < 100000
        printf("%d\n", i)
        i = i + 1
    end
    # for i in range(100000)
    #     print(i, "\n")
    # end
    # let bos = 0
    # alloc_start(bos)

    # let c: int8 = 10
    # let x: fun(_: int8*): int8& = ^test
    # test_ptr(^x, &c)

    ret 0
end