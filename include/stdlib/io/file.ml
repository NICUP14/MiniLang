# file.ml - io file library for ml.
# Provides a frontend for c file-related functions.

import stdlib.c.cdef
import stdlib.c.cstdlib
import stdlib.debug
import stdlib.string
import stdlib.string.backend

# It moves file pointer position to the beginning of the file.
macro c_SEEK_END
    cast("int32", literal("SEEK_END"))
end

# It moves file pointer position to the end of file.
macro c_SEEK_SET
    cast("int32", literal("SEEK_SET"))
end

# Closes the given file stream. Any unwritten buffered data are flushed to the OS. Any unread buffered data are discarded. Can be safely called on closed streams.
macro close_file(_stream)
    if _stream != null
        fclose(_stream)
        _stream = null
    end
end

# Opens a file indicated by filename and returns a file stream associated with that file. mode is used to determine the file access mode. 
fun open_file(filename: int8*, mode: int8*): c_stream
    let st = fopen(filename, mode)
    if st == null
        panicf("No such file '%s'", filename)
    end

    ret st
end

# Overload; Opens a file indicated by filename and returns a file stream associated with that file. mode is automatically set to read.
fun open_file(filename: int8*): c_stream
    ret open_file(filename, "r")
end

# Reads a line from the given stream until a newline or end-of-file is encountered. Returns true on success, false on failure. (false end-of-file is reached)
fun read_line(st: c_stream, s: str, size: int64): bool
    let ln: int8* = fgets(c_str(s), size, st)
    ret ln != null
end

# Reads 'size' bytes from the file associated with the given stream and returns it in string form.
fun read_file(st: c_stream, size: int64): str
    let s = empty_str
    let cs: int8* = malloc(size)

    defer s = str(cs)
    defer free(cs)
    fread(cs, size, 1, st)
    cs[size] = 0
    ret s
end

# Overload; Reads the whole file associated with the given stream and returns it in string form. (size is determined using 'ftell')
fun read_file(st: c_stream): str

    fseek(st, 0, c_SEEK_END)
    let size = ftell(st)
    rewind(st)
    # fseek(st, 0, c_SEEK_SET)

    ret read_file(st, size)
end