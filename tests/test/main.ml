import "../../stdlib/cstdlib"
import "../../stdlib/stddef"
import "../../stdlib/debug"
import "../../stdlib/alloc"

macro _alloc_assert
    printf("Oopsies")
end

fun main: int64
    let c: int8* = null
    alloc_str_pass(c, "Hi")
    alloc_assert
    ret 0
end
end