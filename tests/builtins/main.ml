import "../../debug"
import "../../cstdlib"

fun main(): int64
    let a: int8* = 0
    printf("off_of(a): %lld\n", off_of("a"))
    printf("size_of(a): %lld\n", size_of("a"))
    printf("%s:%s: Test\n", file, fun)
    assert_extra(a != 0, line, file, lineno)
    ret 0
end
end