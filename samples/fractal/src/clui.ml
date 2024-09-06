import stdlib.io.print
import src.cluidefs

macro print_char(_arg)
    printf("%c", _arg)
end

macro print_char(_arg, _other)
    print_char(_arg)
    print_char(_other)
end

macro print_elem(_args)
    print_char(_args)
end

let swap_tmp = 0
macro swap(_arg1, _arg2)
    swap_tmp = _arg1
    _arg1 = _arg2
    _arg2 = swap_tmp
end

fun draw_line(cvs: canvas&, start_pos: canvas_pos&, end_pos: canvas_pos&, elem: int8): void
    let start_pos_col = start_pos.col
    let start_pos_row = start_pos.row
    let end_pos_col = end_pos.col
    let end_pos_row = end_pos.row

    let dx = abs(end_pos_col - start_pos_col)
    let dy = abs(end_pos_row - start_pos_row)

    let sx = 1 if start_pos_col < end_pos_col else 0 - 1
    let sy = 1 if start_pos_row < end_pos_row else 0 - 1
    let err = dx - dy

    while true
        # Plot the point on the canvas
        canvas_set(cvs, canvas_pos(start_pos_row, start_pos_col), elem)

        # If the current point is the end point, break
        if (start_pos_col == end_pos_col && start_pos_row == end_pos_row)
            ret
        end

        let e2 = 2 * err

        # Move in the x-direction
        if e2 > 0 - dy
            err = err - dy
            start_pos_col = start_pos_col + sx
        end

        # Move in the y-direction
        if e2 < dx
            err = err + dx
            start_pos_row = start_pos_row + sy
        end
   end
end

macro pow2(_args)
    _args * _args
end

fun draw_circle(cvs: canvas&, center: canvas_pos&, radius: int64, elem: int8): void
    let col = radius
    let row = 0
    let d = 1 - radius
    
    # Plot the initial points
    canvas_set(cvs, canvas_pos(center.row + row, center.col + col), elem)
    canvas_set(cvs, canvas_pos(center.row + row, center.col - col), elem)
    canvas_set(cvs, canvas_pos(center.row + col, center.col + row), elem)
    canvas_set(cvs, canvas_pos(center.row - col, center.col + row), elem)
    
    if radius > 0
        canvas_set(cvs, canvas_pos(center.row - row, center.col + col), elem)
        canvas_set(cvs, canvas_pos(center.row - row, center.col - col), elem)
        canvas_set(cvs, canvas_pos(center.row - col, center.col + row), elem)
        canvas_set(cvs, canvas_pos(center.row - col, center.col - row), elem)
    end

    # Use symmetry to fill out the circle
    while col > row
        row = row + 1

        if d <= 0
            d = d + 2 * row + 1
        else
            col = col - 1
            d = d + 2 * row - 2 * col + 1
        end
        
        if col < row
            ret
        end
        
        # Plot the points for each octant
        canvas_set(cvs, canvas_pos(center.row + col, center.col + row), elem)
        canvas_set(cvs, canvas_pos(center.row + col, center.col - row), elem)
        canvas_set(cvs, canvas_pos(center.row - col, center.col + row), elem)
        canvas_set(cvs, canvas_pos(center.row - col, center.col - row), elem)

        
        canvas_set(cvs, canvas_pos(center.row + row, center.col + col), elem)
        canvas_set(cvs, canvas_pos(center.row + row, center.col - col), elem)
        canvas_set(cvs, canvas_pos(center.row - row, center.col + col), elem)
        canvas_set(cvs, canvas_pos(center.row - row, center.col - col), elem)
    end
end

fun draw_ugly_circle(cvs: canvas&, center: canvas_pos&, radius: int64, elem: int8)
    for row in range(cvs.height)
        for col in range(cvs.width)
            if pow2(row - center.row) + pow2(col - center.col) <= pow2(radius)
                let elem_ref: int8& = canvas_at(cvs, row, col)
                elem_ref = elem
            end
        end
    end
end

fun fill_canvas(cvs: canvas&, elem: int8)
    memset(cvs.arr, elem, cvs.height * cvs.width)
end

fun show_canvas(cvs: canvas&)
    for row in range(cvs.height)
        for col in range(cvs.width)
            let elem_ref: int8&= canvas_at(cvs, row, col)
            print_elem(elem_ref)
        end
        print("\n")
    end
end