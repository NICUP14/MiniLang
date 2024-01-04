# C standard library functions
extern fun exit(status: int32): void
extern fun printf(msg: int8*, ...): int32
extern fun scanf(format: int8*, ...): int32
extern fun malloc(size: int64): void*
extern fun free(ptr: void*): void
extern fun memset(ptr: void*, value: int32, num: int64): void*
extern fun memcpy(dest: void*, src: void*, num: int64): void*
extern fun strlen(str: int8*): int64
extern fun strcpy(dest: int8*, src: int8*): int8*
extern fun strncpy(dest: int8*, src: int8*, num: int64): int8*
extern fun strcmp(str1: int8*, str2: int8*): int32
extern fun strncmp(str1: int8*, str2: int8*, num: int64): int32
extern fun strcat(dest: int8*, src: int8*): int8*
extern fun strncat(dest: int8*, src: int8*, num: int64): int8*
extern fun strchr(str: int8*, character: int32): int8*
extern fun strrchr(str: int8*, character: int32): int8*
extern fun strstr(str1: int8*, str2: int8*): int8*
extern fun atoi(str: int8*): int32
# extern fun atof(str: int8*): double
extern fun abs(number: int32): int32
extern fun labs(number: int64): int64
extern fun rand(): int32
extern fun srand(seed: int32): void
end