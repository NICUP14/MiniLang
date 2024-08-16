alias int = int32
alias c_str = int8*
extern fun exit(status: int): void
extern fun printf(fmt: c_str, ...): int
extern fun strcmp(str1: c_str, str2: c_str): int
extern fun strcpy(dest: c_str, src: c_str): int
extern fun strcat(dest: c_str, src: c_str): int

let nassert: int64 = 1
fun assert(val: int64): void
    if val == 0
        printf("Failed assertion %lld\n", nassert)
        exit(1)
    end
    nassert = nassert + 1
end

fun main(): int
    let res: int8[100]
    let str1: c_str = "Test "
    let str2: c_str = "Best "
    strcpy(res, str1)
    strcat(res, str2)

    # !BUG: Not working (assert expr)
    printf("Res: %s\n", res)
    assert(strcmp(res, "Test Best") == 0)
    exit(0)
end