import stdlib.io.print

struct _color
    blue: int8*
    cyan: int8*
    green: int8*
    red: int8*
    purple: int8*
    endc: int8*
    bold: int8*
    underline: int8*
end

macro color
    _color(
        "\033[94m",
        "\033[96m",
        "\033[92m",
        "\033[91m",
        "\033[35m",
        "\033[0m",
        "\033[1m",
        "\033[4m"
    )
end

struct canvas_pos
    row: int64
    col: int64
end

fun _print(st: c_stream, pos: canvas_pos&)
    print("canvas_pos(row = ", pos.row, ", col = ", pos.col, ")")
end

fun add(pos1: canvas_pos&, pos2: canvas_pos&)
    ret canvas_pos(pos1.row + pos2.row, pos1.col + pos2.col)
end

struct canvas
    width: int64
    height: int64
    arr: int8*
end

fun copy(arg: canvas&)
    ret canvas(arg.width, arg.height, arg.arr)
end

fun canvas(height: int64, width: int64)
    let arr = alloc_size(width * height)
    ret canvas(width, height, arr)
end

fun canvas_at(cvs: canvas&, pos: canvas_pos): int8&
    ret &(cvs.arr at (pos.row * cvs.width + pos.col))
end

fun canvas_at(cvs: canvas&, row: int64, col: int64): int8&
    ret &(cvs.arr at (row * cvs.width + col))
end

fun canvas_set(cvs: canvas&, pos: canvas_pos&, elem: int8)
    let idx = pos.col + cvs.width * pos.row
    cvs.arr at idx = elem
end