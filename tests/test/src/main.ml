import stdlib.io.read
import stdlib.io.print

fun test
    print("Hello")
end

macro fmacro
    fun test(arg: int64)
        print("Hello ", arg)
    end
end

macro tmacro
    let a = 15
    println a
end


# fmacro

fun main
    tmacro
    test
    ret 0
end