import stdlib.io.read
import stdlib.io.print
import src.fractal

fun handle_help
    let help: c_str = <<-
        Options: mandelbrot, triangle, tree
        Parameters: y x scale
    end
    println(help)
end

fun handle_cmd(cvs: canvas&, cmd: str&): void
    if cmd.equals("mandelbrot")
        mandelbrot_fractal(cvs, '*')
        ret
    end

    let x = 0
    let y = 0
    let scale = 0
    print("Parameters: ")
    read(y, x, scale)

    y = cvs.height - y
    if cmd.equals("triangle")
        triangle_fractal(cvs, canvas_pos(y, x), scale, '*')
    elif cmd.equals("tree")
        tree_fractal(cvs, canvas_pos(y, x), scale, '*')
    else
        panicf("Invalid command %s", cmd)
    end

end

fun main: int32
    # GC needed for stdlib.alloc & stdlib.string
    let bos = 0
    alloc_start(bos)

    let cvs = canvas(100, 120)
    fill_canvas(cvs, ' ')

    println("Canvas size: ", cvs.height, " ", cvs.width)
    print("Option: ")
    let opt = input

    handle_cmd(cvs, opt)
    show_canvas(cvs)

    ret 0
end