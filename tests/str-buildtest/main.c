int dbg.main (int esi, int edx) {
    loc_0x407750:
        // CALL XREF from sym.__tmainCRTStartup @ 0x4013c2(x)
        push  (rsi)   // int32_t main()//
        push  (rbx)
        rsp -= 0x68
        sym.__main  ()
        rbx = var_40h
        edx = 1       // int64_t arg2
        ecx = 0x1e    // 30 // int64_t arg1
        sym.alloc_size_int64_bool_2  () // sym.alloc_size_int64_bool_2(0x0, 0x0)
        rsi = var_20h
        rdx = rbx     // int64_t arg2
        r8d = 0x63    // 'c' // 99 // int64_t arg_28h
        rcx = rsi     // int64_t arg1
        qword [var_50h] = rax
        qword [var_40h] = 0
        qword [var_48h] = 0x1e // [0x1e:8]=-1 // 30
        sym.append_str_buildref_int8_2  () // sym.append_str_buildref_int8_2(0x0, 0x177f98, 0x177fc0, 0x177f98)
        rdx = rbx     // int64_t arg2
        rcx = rsi     // int64_t arg1
        r8d = 0x6f    // 'o' // 111 // int64_t arg_28h
        sym.append_str_buildref_int8_2  () // sym.append_str_buildref_int8_2(0x0, 0x177f98, 0x177fc0, 0x177f98)
        rdx = rbx     // int64_t arg2
        rcx = rsi     // int64_t arg1
        r8d = 0x70    // 'p' // 112 // int64_t arg_28h
        sym.append_str_buildref_int8_2  () // sym.append_str_buildref_int8_2(0x0, 0x177f98, 0x177fc0, 0x177f98)
        rdx = rbx     // int64_t arg2
        rcx = rsi     // int64_t arg1
        r8d = 0x79    // 'y' // 121 // int64_t arg_28h
        sym.append_str_buildref_int8_2  () // sym.append_str_buildref_int8_2(0x0, 0x177f98, 0x177fc0, 0x177f98)
        rdx = rbx     // int64_t arg2
        rcx = rsi     // int64_t arg1
        r8 = rip + str._this_one_also // 0x409966 // " this one also" // int64_t arg3
        sym.append_str_buildref_int8ptr_2  () // sym.append_str_buildref_int8ptr_2(0x0, 0x177f98, 0x177fc0, 0x177f98, 0x409966)
        rcx = rbx     // int64_t arg1
        dbg.to_str_str_buildref_1  () // dbg.to_str_str_buildref_1(0x0)
        rsi = qword [0x004080d0] // [0x4080d0:8]=0x407610 sym.__acrt_iob_func // sym.__acrt_iob_func
        ecx = 1
        rbx = rax
        rsi  ()       // sym.__acrt_iob_func // sym.__acrt_iob_func(0x0)
        r8d = 8       // size_t nitems
        edx = 1       // size_t size
        rcx = rip + str.Result:_ // 0x409975 // "Result: " // const void *ptr
        r9 = rax      // FILE *stream
        sym.fwrite  ()
        // size_t fwrite(0x203a746c75736552, -1, -1, ?)
        rcx = rbx     // int64_t arg1
        dbg.sdsdup  () // dbg.sdsdup(0x0)
        ecx = 1
        rbx = rax
        rsi  ()       // sym.__acrt_iob_func // sym.__acrt_iob_func(0x0)
        rcx = rbx     // const char *s
        rdx = rax     // FILE *stream
        sym.fputs  ()
        // int fputs(-1, ?)
        rcx = rbx     // int64_t arg1
        dbg.sdsfree  () // dbg.sdsfree(0x0)
        rcx = rip + 0x213e // 0x40997e // const char *s
        sym.puts  ()
        // int puts("")
        eax = 0
        rsp += 0x68
        rbx = pop  ()
        rsi = pop  ()
        re
         // (break)
}
