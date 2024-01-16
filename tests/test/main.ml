import "../../cstdlib"

macro print(print_num)
    let idx = 0
    while idx < num
        printf("%lld", idx)
        idx = idx + 1
    end
end

macro x()
    "123"
end

fun main(): int64
    print("Hello", "Hello2")
    let d = x()
    let d = "123"
    idx = 15
    # let x: int64 = 0
    # let _ = 1

    # block myblock
    #     let x = 0
    #     let y = 0
    # end

    # block _
    #     let x = 0
    #     let y = 0
    # end

    ret 0
end
end