import "../../cstdlib"

namespace main
fun main(): int64
    let x: int64 = 0
    let l1 = 1
    block myblock
    let x = 0
    let y = 0
    end
    block
    let x = 0
    let y = 0
    end
    ret 0
end
end
end