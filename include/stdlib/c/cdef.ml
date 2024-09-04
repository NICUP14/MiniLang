extern struct FILE;

# C standard library types
alias c_void = void
alias c_char  = int8
alias c_short = int16
alias c_int   = int32
alias c_long  = int32
alias c_long_long = int64
alias c_str = int8*
alias c_stream = FILE*

# C type sizes (implementation-defined)
macro c_ptr_size
    cast("int64", literal("sizeof(void*)"))
end
macro c_char_size
    cast("int64", literal("sizeof(char)"))
end
macro c_short_size
    cast("int64", literal("sizeof(short)"))
end
macro c_int_size
    cast("int64", literal("sizeof(int)"))
end
macro c_long_size
    cast("int64", literal("sizeof(long)"))
end
macro c_long_long_size
    cast("int64", literal("sizeof(long long)"))
end

# C standard library macros
macro null
    cast("void*", 0)
end
macro stdin
    cast("c_stream", literal("stdin"))
end
macro stdout
    cast("c_stream", literal("stdout"))
end
macro stderr
    cast("c_stream", literal("stderr"))
end