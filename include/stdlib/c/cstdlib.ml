import stdlib.c.cdef

# C standard library functions
extern fun exit(status: int32): void
extern fun getchar: int32
extern fun printf(msg: int8*, ...): int32
extern fun fprintf(st: c_stream, msg: int8*, ...): int32
extern fun scanf(format: int8*, ...): int32
extern fun fscanf(st: c_stream, format: int8*, ...): int32
extern fun puts(str: int8*): int32
extern fun malloc(size: int64): void*
extern fun calloc(num: int64, size: int64): void*
extern fun realloc(ptr: void*, size: int64): void*
extern fun free(ptr: void*): void
extern fun memset(ptr: void*, value: int32, num: int64): void*
extern fun memcpy(dest: void*, src: void*, num: int64): void*
extern fun strlen(str: int8*): int64
extern fun strdup(str: int8*): int8*
extern fun strcpy(dest: int8*, src: int8*): int8*
extern fun strncpy(dest: int8*, src: int8*, num: int64): int8*
extern fun strcmp(str1: int8*, str2: int8*): int32
extern fun strncmp(str1: int8*, str2: int8*, num: int64): int32
extern fun strcat(dest: int8*, src: int8*): int8*
extern fun strncat(dest: int8*, src: int8*, num: int64): int8*
extern fun strchr(str: int8*, character: int32): int8*
extern fun strrchr(str: int8*, character: int32): int8*
extern fun strstr(str1: int8*, str2: int8*): int8*
extern fun strtoll(str1: int8*, str_end: int8*, base: int64): int32
extern fun isdigit(arg: int32): int32
extern fun isspace(arg: int32): int32
extern fun atoi(str: int8*): int32
# extern fun atof(str: int8*): double
extern fun abs(number: int32): int32
extern fun labs(number: int64): int64
extern fun rand(): int32
extern fun srand(seed: int32): void
extern fun dup(st: c_stream): c_stream
extern fun fopen(filename: int8*, mode: int8*): void*
extern fun fclose(st: c_stream): int32
extern fun fgets(ptr: void*, size: int64, st: c_stream): int8*
extern fun fread(ptr: void*, size: int64, cnt: int64, st: c_stream): int64
extern fun fwrite(ptr: void*, size: int64, cnt: int64, st: c_stream): int64
extern fun fseek(st: c_stream, offset: int64, origin: int32): int32
extern fun ftell(st: c_stream): int64
extern fun rewind(st: c_stream): void
extern fun remove(filename: int8*): int32
extern fun rename(oldname: int8*, newname: int8*): int32