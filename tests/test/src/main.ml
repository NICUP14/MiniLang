import stdlib.io.read
import stdlib.io.print

let falltrough = false
macro switch(_ident2, _cond2, _body2)
    if (_ident2 == _cond2) || falltrough
        falltrough = true
        _body2
    end

end

macro switch(_ident, _cond, _body, _other)
    switch(_ident, _cond, _body)
    switch(_ident, _other)
end

macro break
    falltrough = false
end

macro add_args
    1
    2
end

macro sum(_arg1, _arg2)
    _arg1 + _arg2
end

macro sum(_arg1, _arg2, _arg3)
    _arg1 + sum(_arg2, _arg3)
end

fun main
    # let a = 0
    # read(a)

    # switch(a,
    #     (15, 
    #         group(
    #             print("Is 15"), 
    #             break)),
    #     (16, 
    #         group(
    #             print("Is 16"), 
    #             print("Also 16"), 
    #             print("Also 166"))),
    #     (17, 
    #         print("Is 17")),
    #     (18, 
    #         print("Is 18")),
    #     (19, 
    #         print("Is 19")),
    #     (20, 
    #         print("Is 20"))
    # )
    ret 0
end