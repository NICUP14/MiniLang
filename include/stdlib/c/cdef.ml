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