typedef int = int32
typedef cstr = int8*
extern fun exit(status: int): void
extern fun printf(fmt: cstr, ...): int
extern fun strcpy(dest: cstr, src: cstr): int

let nassert: int64 = 1
fun assert(val: int64): void
    if val == 0
        printf("Failed assertion %lld\n", nassert)
        exit(1)
    end
    nassert = nassert + 1
end

fun main(): int64
    let my_str: cstr = <<-
        \end
        HELLO end
        HELLO WORLD
        HELLO FROM BELOW
    end
    ret 0
end
end