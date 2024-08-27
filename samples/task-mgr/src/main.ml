import stdlib.c.cdef
import stdlib.string
import stdlib.io.read
import stdlib.io.print
import src.task

macro not(_arg)
    false if _arg else true
end

fun main
    let bos = 0
    alloc_start(bos)

    let full_cmd = empty_str
    let tsk_list = task_list_new
    while true
        full_cmd = input.trim("\n")
        if full_cmd.equals("exit".str)
            panic("main: Exit called")
        end

        handle_cmd(tsk_list, full_cmd)
    end

    ret 0
end 