import stdlib.io.print

fun main: int32
    # Starts the garbage collector 
    let bos = 0
    alloc_start(bos)

    # Your code here
    println "HelloWorld"

    ret 0
end