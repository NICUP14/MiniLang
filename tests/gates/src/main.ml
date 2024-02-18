import "stdlib/cstdlib"

fun not(t: bool): bool
    if t
        ret false
    else
        ret true
    end
end

fun and(t1: bool, t2: bool): bool
    if t1
        if t2
            ret true
        else
            ret false
        end
    else
        ret false
    end
end

fun bool_str(t: bool): int8*
    if t
        ret "true"
    else
        ret "false"
    end
end

fun print_bool(t: bool): void
    puts(bool_str(t))
end

fun _print_nand(t1: bool, t2: bool): void
    printf("%s↑%s", bool_str(t1), bool_str(t2))
end

macro nand(_t1, _t2)
    not(and(_t1, _t2))
end

macro nand(_t1, _t2, _t3)
    nand(nand(_t1, _t2), _t3)
end

macro print_rev(_t)
    printf("%lld", _t)
end

macro print_rev(_t1, _t2)
    if _t1 > 0
        print_rev(_t2)
    end
end

fun main: int64
    let b = and(true, true)
    let a = (nand(true, true, false))
    print_bool(a)
    print_rev(5, 4, 3, 2, 1)
end
end