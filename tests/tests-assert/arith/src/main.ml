import "stdlib/debug"

macro equation
    ((10 * 5) - (6 / 2)) + (8 * (4 / 2)) - (5 + 3)
end

macro equation2
    (20 / 4) * ((15 - 3) + (6 * 2)) - (10 + 5)
end

macro equation3
    ((20 / 3) % 2) + ((30 / 4) % 3)
end

macro equation4
    ((35 / 6) * 4)+((28 / 5) % 3)
end

fun main: int64
    assert(equation == 55)
    assert(equation2 == 105)
    assert(equation3 == 1)
    assert(equation4 == 22)
    ret 0
end
end