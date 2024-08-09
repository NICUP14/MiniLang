import "stdlib/print"
import "stdlib/c/cstdarg"

# fun var(first: int64, ...): void
#     let listx: va_list
#     init(listx, first)
#     defer listx.deinit
#     listx.get_int64.print
#     listx.get_int64.print
# end

namespace nsp
    namespace nsp2
        let e = 200

        fun hello2: void
            print "Hi"
        end
    end

    let a = 100

    fun hello: void
        print "Hi"
    end
end

fun main: int32
    let b = 16
    let c = 15 if b == 16 else 20
    # nsp.nsp2.e.print
    nsp.hello
    nsp.nsp2.hello2
    # c.print
    ret 0
end
