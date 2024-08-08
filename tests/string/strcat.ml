alias int = int32
alias cstr = int8*
extern fun exit(status: int): void
extern fun printf(fmt: cstr, ...): int
extern fun strcmp(str1: cstr, str2: cstr): int
extern fun strcpy(dest: cstr, src: cstr): int
extern fun strcat(dest: cstr, src: cstr): int

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
    let str1: cstr = "Test "
    let str2: cstr = "Best "
    strcpy(res, str1)
    strcat(res, str2)

    # !BUG: Not working (assert expr)
    printf("Res: %s\n", res)
    assert(strcmp(res, "Test Best") == 0)
    exit(0)
end