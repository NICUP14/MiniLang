import src.cluidefs
import src.clui

# Integer-based fixed-point representation
macro max_iter
    100000
end
macro scale_factor
    10000
end
macro X_MIN 
    ((0 - 2) * scale_factor)
end
macro X_MAX
    (1 * scale_factor)
end
macro Y_MIN
    ((0 - 1) * scale_factor)
end
macro Y_MAX
    (1 * scale_factor)
end

# Function to map terminal coordinates to the Mandelbrot set's range in fixed-point
fun map_to_real(x: int64, width: int64, min_r: int64, max_r: int64)
    ret min_r + (x * (max_r - min_r) / width);
end

fun map_to_imaginary(y: int64, height: int64, min_i: int64, max_i: int64)
    ret min_i + (y * (max_i - min_i) / height);
end

# function to determine if a point is in the mandelbrot set
fun mandelbrot(cvs: canvas&, start_pos: canvas_pos&)
    let zr = 0
    let zi = 0
    let cr = (start_pos.col - cvs.width / 2) * scale_factor
    let ci = (start_pos.row - cvs.height / 2) * scale_factor
    
    for it in range(max_iter)
        # calculate square of the magnitude
        let zr2 = (zr / scale_factor) * (zr / scale_factor)
        let zi2 = (zi / scale_factor) * (zi / scale_factor)
        
        if zr2 + zi2 > (4 * scale_factor * scale_factor)
            ret it
        end
        
        # calculate new zr and zi
        let new_zr = (zr2 - zi2 + cr) / scale_factor
        let new_zi = (2 * zr * zi + ci) / scale_factor
        
        zr = new_zr
        zi = new_zi
    end

    ret it
end

fun mandelbrot_elem(it: int64): int8
    if it == max_iter
        ret ' '
    elif it > 750000
        ret '@'
    elif it > 500000
        ret '#'
    elif it > 100000
        ret '%'
    elif it > 50000
        ret '&'
    elif it > 10000
        ret '8'
    elif it > 1000
        ret '+'
    elif it > 500
        ret '='
    elif it > 250
        ret '*'
    elif it > 50
        ret '-'
    elif it > 20
        ret ':'
    elif it > 10
        ret '.'
    end

    ret '#'
end

fun mandelbrot_fractal(cvs: canvas&, elem: int8): void
    for row in range(cvs.height)
        for col in range(cvs.width)
            let cr = map_to_real(col, cvs.width, X_MIN, X_MAX);
            let ci = map_to_imaginary(row, cvs.height, Y_MIN, Y_MAX);
            let it = mandelbrot(cvs, canvas_pos(cr, ci))
            canvas_set(cvs, canvas_pos(row, col), mandelbrot_elem(it))
        end
    end
end

fun triangle_fractal(cvs: canvas&, start_pos: canvas_pos&, scale: int64, elem: int8): void
    if scale == 0
        ret
    end

    let left_edge = start_pos
    let right_edge = start_pos.add(canvas_pos(0, scale))
    
    let height = 86602540378 * scale / 100000000000
    let top_edge = start_pos.add(canvas_pos(0 - height, scale / 2))

    draw_line(cvs, left_edge, right_edge, elem)
    draw_line(cvs, left_edge, top_edge, elem)
    draw_line(cvs, right_edge, top_edge, elem)

    triangle_fractal(cvs, left_edge, scale / 2, elem)
    triangle_fractal(cvs, left_edge.add(canvas_pos(0, scale / 2)), scale / 2, elem)
    triangle_fractal(cvs, left_edge.add(canvas_pos(0 - height / 2, scale / 4)), scale / 2, elem)
end

fun tree_fractal(cvs: canvas&, start_pos: canvas_pos&, scale: int64, elem: int8, wait: bool): void
    if scale == 0
        ret
    end

    let s: str = empty_str
    if wait
        show_canvas(cvs)
        s = input
    end

    let end_pos = start_pos.add(canvas_pos(0 - scale, 0))
    let center = end_pos.add(canvas_pos(0 - scale, 0))
    draw_line(cvs, start_pos, end_pos, elem)
    draw_circle(cvs, center, scale, elem)

    let left = center.add(canvas_pos(0, scale))
    let right = center.add(canvas_pos(0, 0 - scale))
    draw_line(cvs, end_pos, left, elem)
    draw_line(cvs, end_pos, right, elem)

    tree_fractal(cvs, left, scale - 2, elem, wait)
    tree_fractal(cvs, right, scale - 2, elem, wait)

end

fun tree_fractal(cvs: canvas&, start_pos: canvas_pos&, scale: int64, elem: int8): void
    tree_fractal(cvs, start_pos, scale, elem, false)
end