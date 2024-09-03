import stdlib.debug
import stdlib.string

macro not(_arg)
    false if _arg else true
end

macro neg(_arg)
    _arg = not(_arg)
end

macro incr(_arg)
    *_arg = *_arg + 1
end

macro decr(_arg)
    *_arg = *_arg - 1
end                                                  

struct task
    name: str
    status: bool
    visible: bool
end

struct task_list
    arr: task*
    arr_len: int64*
end

fun copy(tsk: task&): task
    ret task(tsk.name, tsk.status, tsk.visible)
end

fun task(name: str)
    ret task(name, false, true)
end

fun len(tsk_list: task_list&)
    ret *tsk_list.arr_len
end

fun task_list_new
    let new_len: int64* = null
    let new_arr: task[100]* = null
    new_len.alloc
    new_arr.alloc

    *new_len = 0
    ret task_list(new_arr, new_len)
end

macro task_at(_list, _idx)
    _list.arr at _idx
end

fun list_task(tsk_list: task_list&)
    for it in range(tsk_list.len)
        let tsk = task_at(tsk_list, it)

        if tsk.visible
            let stat_str = "[X]" if tsk.status else "[ ]"
            println(it, ". ", stat_str, " ", tsk.name)
        end
    end
end

fun find_task(tsk_list: task_list&, tsk_name: str&): int64
    for it in range(tsk_list.len)
        if tsk_name.equals(task_at(tsk_list, it).name)
            ret it
        end
    end

    ret 0 - 1
end

fun add_task(tsk_list: task_list&, tsk: task)
    let idx = find_task(tsk_list, tsk.name)
    if idx != 0 - 1
        if task_at(tsk_list, idx).visible
            ret false
        else
            task_at(tsk_list, idx).visible = true
            ret true
        end
    end

    tsk_list.arr[tsk_list.len] = tsk
    tsk_list.arr_len.incr
    ret true
end

fun handle_help
    let help_msg: c_str = <<-
        taskmgr: Simple CRUD interface for managing tasks.
        version: 1.0.0
        list - List all tasks.
        add 'task' - Add task named mytask.
        remove 'task' - Remove task named mytask.
        complete 'task' - Complete/Uncomplete task named mytask.
        help - Print this message.
    end

    print(help_msg)
end

fun handle_list(tsk_list: task_list&)
    tsk_list.list_task
end

fun handle_add(tsk_list: task_list&, cmd: str&, args: str&)
    let task_name = args.trim("'")
    let stat = tsk_list.add_task(task(task_name))

    if stat
        println("handle_add: Succesfully added task: ", args)
    else
        println("handle_add: Task already exists: ", args)
    end
end

fun handle_complete(tsk_list: task_list&, cmd: str&, args: str&)
    let task_name = args.trim("'")
    let idx = tsk_list.find_task(task_name)
    
    if idx == 0 - 1 && not(task_at(tsk_list, idx).visible)
        print("handle_complete: Task does not exist: ", args)
    else
        task_at(tsk_list, idx).status.neg
        println("handle_complete: Succesfully completed task: ", args)
    end
end

fun handle_remove(tsk_list: task_list&, cmd: str&, args: str&)
    let task_name = args.trim("'")
    let idx = tsk_list.find_task(task_name)

    if idx == 0 - 1
        print("handle_remove: Task does not exist: ", args)
    else
        task_at(tsk_list, idx).visible.neg
        task_at(tsk_list, idx).status = false
        println("handle_remove: Succesfully removed task: ", args)
    end
end

fun handle_cmd(tsk_list: task_list&, full_cmd: str)
        let sep = full_cmd.find(" ")
        let cmd_idx = sep - 1 if sep != 0 - 1 else 0 - 1
        let cmd: str = substr(full_cmd, 0, cmd_idx)

        if cmd.equals("help".str)
            handle_help
        elif cmd.equals("list".str)
            tsk_list.handle_list
        else
            assert(sep != 0 - 1)
            let args = substr(full_cmd, sep + 1, 0 - 1)

            if cmd.equals("add".str)
                tsk_list.handle_add(cmd, args)
            elif cmd.equals("complete".str)
                tsk_list.handle_complete(cmd, args)
            elif cmd.equals("remove".str)
                tsk_list.handle_remove(cmd, args)
            else
                println("Command: ", cmd, " ", args)
                panic("handle_cmd: Invalid command")
            end

        end

        println("")
end