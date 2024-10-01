import stdlib.io.print
import src.str_build

fun main: int32
    # Starts the garbage collector 
    let bos = 0
    alloc_start(bos)

    let sb = str_build(30)
    sb.append('c')
    sb.append('o')
    sb.append('p')
    sb.append('y')
    sb.append(" this one also")
    
    println("Result: ", sb.to_str)

    ret 0
end