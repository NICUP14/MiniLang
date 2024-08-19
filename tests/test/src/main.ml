import stdlib.debug
import stdlib.io.print
import stdlib.c.cstdlib

macro panic_exit
    print("Super custom panic message!")
    exit(1)
end

fun main
    panic("Oh no!")
    ret 0
end