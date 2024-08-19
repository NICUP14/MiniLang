#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define GC_NO_GLOBAL_GC
#include <gc.h>
#include <mlalloc.h>
GarbageCollector ml_gc;
#define ML_ALLOC_GC
#include <stdarg.h>
#define c_va_start va_start
#define c_va_arg va_arg
void* va_arg_va_list_voidptr(va_list va_arg_va_list_voidptr_list, void* va_arg_va_list_voidptr_argx) { 
  return c_va_arg(va_arg_va_list_voidptr_list, void*);
}

long long va_arg_va_list_int64(va_list va_arg_va_list_int64_list, long long va_arg_va_list_int64_argx) { 
  return (long long)c_va_arg(va_arg_va_list_int64_list, long long);
}

#include <sds.h>
char* c_str_sds(sds c_str_sds_s) { 
  return (char*)c_str_sds_s;
}

sds str_int8ptr(char* str_int8ptr_s) { 
  return sdsnew(str_int8ptr_s);
}

sds str_sds(sds str_sds_s) { 
  return str_int8ptr(c_str_sds(str_sds_s));
}

sds str_from_int8ptr(char* str_from_int8ptr_fmt, ...) { 
  va_list str_from_int8ptr_listx;
  c_va_start(str_from_int8ptr_listx, (long long)str_from_int8ptr_fmt);
  return sdscatvprintf(sdsempty(), str_from_int8ptr_fmt, str_from_int8ptr_listx);
}

sds empty_str() { 
  return sdsempty();
}

sds extend_sds_int64(sds extend_sds_int64_s, long long extend_sds_int64_size) { 
  return sdsgrowzero(extend_sds_int64_s, extend_sds_int64_size);
}

sds clone_sds(sds clone_sds_s) { 
  return sdsdup(clone_sds_s);
}

void clear_sds(sds clear_sds_s) { 
  sdsclear(clear_sds_s);
}

sds copy_sds_sds(sds copy_sds_sds_s, sds copy_sds_sds_t) { 
  return sdscpy(copy_sds_sds_s, c_str_sds(copy_sds_sds_t));
}

long long len_sds(sds len_sds_s) { 
  return sdslen(len_sds_s);
}

sds substr_sds_int64_int64(sds substr_sds_int64_int64_s, long long substr_sds_int64_int64_start, long long substr_sds_int64_int64_send) { 
  sds substr_sds_int64_int64_tmp = str_sds(substr_sds_int64_int64_s);
  sdsrange(substr_sds_int64_int64_tmp, substr_sds_int64_int64_start, substr_sds_int64_int64_send);
  return substr_sds_int64_int64_tmp;
}

sds concat_sds_sds(sds concat_sds_sds_s, sds concat_sds_sds_t) { 
  sds concat_sds_sds_tmp = str_sds(concat_sds_sds_s);
  return sdscatsds(concat_sds_sds_tmp, concat_sds_sds_t);
}

sds concat_from_sds_int8ptr(sds concat_from_sds_int8ptr_s, char* concat_from_sds_int8ptr_fmt, ...) { 
  va_list concat_from_sds_int8ptr_listx;
  c_va_start(concat_from_sds_int8ptr_listx, (long long)concat_from_sds_int8ptr_fmt);
  sds concat_from_sds_int8ptr_tmp = str_sds(concat_from_sds_int8ptr_s);
  return sdscatvprintf(concat_from_sds_int8ptr_tmp, concat_from_sds_int8ptr_fmt, concat_from_sds_int8ptr_listx);
}

sds trim_sds_int8ptr(sds trim_sds_int8ptr_s, char* trim_sds_int8ptr_cset) { 
  sds trim_sds_int8ptr_tmp = str_sds(trim_sds_int8ptr_s);
  return sdstrim(trim_sds_int8ptr_tmp, trim_sds_int8ptr_cset);
}

int compare_sds_sds(sds compare_sds_sds_s, sds compare_sds_sds_s2) { 
  return sdscmp(compare_sds_sds_s, compare_sds_sds_s2);
}

char equals_sds_sds(sds equals_sds_sds_s, sds equals_sds_sds_s2) { 
  return ((long long)sdscmp(equals_sds_sds_s, equals_sds_sds_s2) == 0);
}

sds to_lower_sds(sds to_lower_sds_s) { 
  sdstolower(to_lower_sds_s);
  return to_lower_sds_s;
}

sds to_upper_sds(sds to_upper_sds_s) { 
  sdstoupper(to_upper_sds_s);
  return to_upper_sds_s;
}

long long find_sds_sds(sds find_sds_sds_s, sds find_sds_sds_sub) { 
  char* find_sds_sds_cs = c_str_sds(find_sds_sds_s);
  char* find_sds_sds_ptr = strstr(find_sds_sds_cs, c_str_sds(find_sds_sds_sub));
  return ((find_sds_sds_ptr == (void*)0) ? (0 - 1) : ((long long)find_sds_sds_ptr - (long long)find_sds_sds_cs));
}

* split_int8ptr_int8ptr_int32ptr(char* split_int8ptr_int8ptr_int32ptr_cs, char* split_int8ptr_int8ptr_int32ptr_sep, int* split_int8ptr_int8ptr_int32ptr_cnt) { 
  sds* split_int8ptr_int8ptr_int32ptr_arr = sdssplitlen(split_int8ptr_int8ptr_int32ptr_cs, strlen(split_int8ptr_int8ptr_int32ptr_cs), split_int8ptr_int8ptr_int32ptr_sep, strlen(split_int8ptr_int8ptr_int32ptr_sep), split_int8ptr_int8ptr_int32ptr_cnt);
  if (split_int8ptr_int8ptr_int32ptr_arr == (void*)0) {
          printf("%s\n", "Cannot split string.");
    printf("Panicked in function %s, %s:%lld\n", "split_int8ptr_int8ptr_int32ptr", "../../include/stdlib/string.ml", 191);
    exit(1);
    }
  return split_int8ptr_int8ptr_int32ptr_arr;
}

* split_sds_sds_int32ptr(sds split_sds_sds_int32ptr_s, sds split_sds_sds_int32ptr_sep, int* split_sds_sds_int32ptr_cnt) { 
  sds* split_sds_sds_int32ptr_arr = sdssplitlen(c_str_sds(split_sds_sds_int32ptr_s), len_sds(split_sds_sds_int32ptr_s), c_str_sds(split_sds_sds_int32ptr_sep), len_sds(split_sds_sds_int32ptr_sep), split_sds_sds_int32ptr_cnt);
  if (split_sds_sds_int32ptr_arr == (void*)0) {
          printf("%s\n", "Cannot split string.");
    printf("Panicked in function %s, %s:%lld\n", "split_sds_sds_int32ptr", "../../include/stdlib/string.ml", 203);
    exit(1);
    }
  return split_sds_sds_int32ptr_arr;
}

* split_sds_int8ptr_int32ptr(sds split_sds_int8ptr_int32ptr_s, char* split_sds_int8ptr_int32ptr_sep, int* split_sds_int8ptr_int32ptr_cnt) { 
  sds* split_sds_int8ptr_int32ptr_arr = sdssplitlen(c_str_sds(split_sds_int8ptr_int32ptr_s), len_sds(split_sds_int8ptr_int32ptr_s), split_sds_int8ptr_int32ptr_sep, strlen(split_sds_int8ptr_int32ptr_sep), split_sds_int8ptr_int32ptr_cnt);
  if (split_sds_int8ptr_int32ptr_arr == (void*)0) {
          printf("%s\n", "Cannot split string.");
    printf("Panicked in function %s, %s:%lld\n", "split_sds_int8ptr_int32ptr", "../../include/stdlib/string.ml", 215);
    exit(1);
    }
  return split_sds_int8ptr_int32ptr_arr;
}

sds join_voidptr_int32_int8ptr(void* join_voidptr_int32_int8ptr_argv, int join_voidptr_int32_int8ptr_argc, char* join_voidptr_int32_int8ptr_sep) { 
  return sdsjoin(join_voidptr_int32_int8ptr_argv, join_voidptr_int32_int8ptr_argc, join_voidptr_int32_int8ptr_sep);
}

sds to_str_bool(char to_str_bool_value) { 
  if (to_str_bool_value == true) {
          return str_int8ptr("true");
    }
  else {
     return str_int8ptr("false");
    }
}

sds to_str_int64(long long to_str_int64_value) { 
  return sdsfromlonglong(to_str_int64_value);
}

sds to_str_voidptr(void* to_str_voidptr_value) { 
  return str_from_int8ptr("%p", to_str_voidptr_value);
}

FILE* open_file_int8ptr_int8ptr(char* open_file_int8ptr_int8ptr_filename, char* open_file_int8ptr_int8ptr_mode) { 
  void* open_file_int8ptr_int8ptr_st = fopen(open_file_int8ptr_int8ptr_filename, open_file_int8ptr_int8ptr_mode);
  if (open_file_int8ptr_int8ptr_st == (void*)0) {
          printf("No such file '%s'", open_file_int8ptr_int8ptr_filename);
    printf("\n");
    printf("Panicked in function %s, %s:%lld\n", "open_file_int8ptr_int8ptr", "../../include/stdlib/io/fio.ml", 29);
    exit(1);
    }
  return open_file_int8ptr_int8ptr_st;
}

FILE* open_file_int8ptr(char* open_file_int8ptr_filename) { 
  return open_file_int8ptr_int8ptr(open_file_int8ptr_filename, "r");
}

char read_line_FILEptr_sds_int64(FILE* read_line_FILEptr_sds_int64_st, sds read_line_FILEptr_sds_int64_s, long long read_line_FILEptr_sds_int64_size) { 
  char* read_line_FILEptr_sds_int64_ln = fgets(c_str_sds(read_line_FILEptr_sds_int64_s), read_line_FILEptr_sds_int64_size, read_line_FILEptr_sds_int64_st);
  return (read_line_FILEptr_sds_int64_ln != (void*)0);
}

sds read_file_FILEptr_int64(FILE* read_file_FILEptr_int64_st, long long read_file_FILEptr_int64_size) { 
  sds read_file_FILEptr_int64_s = empty_str();
  char* read_file_FILEptr_int64_cs = malloc(read_file_FILEptr_int64_size);
  fread(read_file_FILEptr_int64_cs, read_file_FILEptr_int64_size, 1, read_file_FILEptr_int64_st);
  (read_file_FILEptr_int64_cs[read_file_FILEptr_int64_size] = 0);
  (read_file_FILEptr_int64_s = str_int8ptr(read_file_FILEptr_int64_cs));
  free(read_file_FILEptr_int64_cs);
  return read_file_FILEptr_int64_s;
}

sds read_file_FILEptr(FILE* read_file_FILEptr_st) { 
  fseek(read_file_FILEptr_st, 0, (int)SEEK_END);
  long long read_file_FILEptr_size = ftell(read_file_FILEptr_st);
  rewind(read_file_FILEptr_st);
  return read_file_FILEptr_int64(read_file_FILEptr_st, read_file_FILEptr_size);
}

char* _print_sep = (void*)0;
void _print_FILEptr_int64(FILE* _print_FILEptr_int64_st, long long _print_FILEptr_int64_arg) { 
  fprintf(_print_FILEptr_int64_st, "%lld", _print_FILEptr_int64_arg);
}

void _print_FILEptr_int32(FILE* _print_FILEptr_int32_st, int _print_FILEptr_int32_arg) { 
  fprintf(_print_FILEptr_int32_st, "%d", _print_FILEptr_int32_arg);
}

void _print_FILEptr_int16(FILE* _print_FILEptr_int16_st, short _print_FILEptr_int16_arg) { 
  fprintf(_print_FILEptr_int16_st, "%hd", _print_FILEptr_int16_arg);
}

void _print_FILEptr_int8(FILE* _print_FILEptr_int8_st, char _print_FILEptr_int8_arg) { 
  fprintf(_print_FILEptr_int8_st, "%hhd", _print_FILEptr_int8_arg);
}

void _print_FILEptr_sds(FILE* _print_FILEptr_sds_st, sds _print_FILEptr_sds_arg) { 
  fprintf(_print_FILEptr_sds_st, "%s", c_str_sds(_print_FILEptr_sds_arg));
}

void _print_FILEptr_int8ptr(FILE* _print_FILEptr_int8ptr_st, char* _print_FILEptr_int8ptr_arg) { 
  fprintf(_print_FILEptr_int8ptr_st, "%s", _print_FILEptr_int8ptr_arg);
}

void _print_FILEptr_voidptr(FILE* _print_FILEptr_voidptr_st, void* _print_FILEptr_voidptr_arg) { 
  fprintf(_print_FILEptr_voidptr_st, "%p", _print_FILEptr_voidptr_arg);
}

void _print_FILEptr_bool(FILE* _print_FILEptr_bool_st, char _print_FILEptr_bool_arg) { 
  if (_print_FILEptr_bool_arg == true) {
      fprintf(_print_FILEptr_bool_st, "true");
    }
  else if (_print_FILEptr_bool_arg == false) {
   fprintf(_print_FILEptr_bool_st, "false");
    }
  else {
     printf("%s\n", "Logic error");
  printf("Panicked in function %s, %s:%lld\n", "_print_FILEptr_bool", "../../include/stdlib/io/print.ml", 36);
  exit(1);
    }
}

typedef struct {
 long long range_idx;
long long range_start;
long long range_stop;;
} range;

range range_int64_int64_int64(long long range_idx, long long range_start, long long range_stop) { 
  range range_tmp;
  (range_tmp.range_idx = range_idx);
  (range_tmp.range_start = range_start);
  (range_tmp.range_stop = range_stop);
  return range_tmp;
}
range range_int64_int64(long long range_start, long long range_stop) { 
  return range_int64_int64_int64(0, range_start, range_stop);
}

range range_int64(long long range_stop) { 
  return range_int64_int64_int64(0, 0, range_stop);
}

range iter_range(range iter_range_arg) { 
  return iter_range_arg;
}

long long start_rangeref(range* start_rangeref_arg) { 
  return (*start_rangeref_arg).range_start;
}

char stop_rangeref(range* stop_rangeref_arg) { 
  return ((*stop_rangeref_arg).range_idx < (*stop_rangeref_arg).range_stop);
}

long long next_rangeref(range* next_rangeref_arg) { 
  ((*next_rangeref_arg).range_idx = ((*next_rangeref_arg).range_idx + 1));
  return (*next_rangeref_arg).range_idx;
}

typedef struct {
 FILE* file_range_st;
char* file_range_str;
char file_range_succ;;
} file_range;

file_range file_range_FILEptr_int8ptr_bool(FILE* file_range_st, char* file_range_str, char file_range_succ) { 
  file_range file_range_tmp;
  (file_range_tmp.file_range_st = file_range_st);
  (file_range_tmp.file_range_str = file_range_str);
  (file_range_tmp.file_range_succ = file_range_succ);
  return file_range_tmp;
}
file_range lines_FILEptr(FILE* lines_FILEptr_arg) { 
  sds lines_FILEptr_s = empty_str();
  (lines_FILEptr_s = extend_sds_int64(lines_FILEptr_s, 256));
  char lines_FILEptr_succ = read_line_FILEptr_sds_int64(lines_FILEptr_arg, lines_FILEptr_s, 256);
  return file_range_FILEptr_int8ptr_bool(lines_FILEptr_arg, c_str_sds(lines_FILEptr_s), lines_FILEptr_succ);
}

file_range iter_file_range(file_range iter_file_range_arg) { 
  return iter_file_range_arg;
}

sds next_file_rangeref(file_range* next_file_rangeref_arg) { 
  sds next_file_rangeref_s = empty_str();
  (next_file_rangeref_s = extend_sds_int64(next_file_rangeref_s, 256));
  char next_file_rangeref_succ = read_line_FILEptr_sds_int64((*next_file_rangeref_arg).file_range_st, next_file_rangeref_s, 256);
  ((*next_file_rangeref_arg).file_range_str = c_str_sds(next_file_rangeref_s));
  ((*next_file_rangeref_arg).file_range_succ = next_file_rangeref_succ);
  return next_file_rangeref_s;
}

sds start_file_rangeref(file_range* start_file_rangeref_arg) { 
  if ((*start_file_rangeref_arg).file_range_succ == false) {
          printf("%s\n", "Attempt to read from empty file");
    printf("Panicked in function %s, %s:%lld\n", "start_file_rangeref", "../../include/stdlib/builtin/for.ml", 71);
    exit(1);
    }
  sds start_file_rangeref_s = str_int8ptr((*start_file_rangeref_arg).file_range_str);
  next_file_rangeref(start_file_rangeref_arg);
  return start_file_rangeref_s;
}

char stop_file_rangeref(file_range* stop_file_rangeref_arg) { 
  return ((*stop_file_rangeref_arg).file_range_succ == true);
}

typedef struct {
 char* c_str_range_str;
long long c_str_range_idx;
long long c_str_range_start;
long long c_str_range_stop;;
} c_str_range;

c_str_range c_str_range_int8ptr_int64_int64_int64(char* c_str_range_str, long long c_str_range_idx, long long c_str_range_start, long long c_str_range_stop) { 
  c_str_range c_str_range_tmp;
  (c_str_range_tmp.c_str_range_str = c_str_range_str);
  (c_str_range_tmp.c_str_range_idx = c_str_range_idx);
  (c_str_range_tmp.c_str_range_start = c_str_range_start);
  (c_str_range_tmp.c_str_range_stop = c_str_range_stop);
  return c_str_range_tmp;
}
c_str_range iter_int8ptr(char* iter_int8ptr_arg) { 
  return c_str_range_int8ptr_int64_int64_int64(iter_int8ptr_arg, 0, 0, strlen(iter_int8ptr_arg));
}

char start_c_str_rangeref(c_str_range* start_c_str_rangeref_arg) { 
  return (*start_c_str_rangeref_arg).c_str_range_str[(*start_c_str_rangeref_arg).c_str_range_start];
}

char stop_c_str_rangeref(c_str_range* stop_c_str_rangeref_arg) { 
  return ((*stop_c_str_rangeref_arg).c_str_range_idx < (*stop_c_str_rangeref_arg).c_str_range_stop);
}

char next_c_str_rangeref(c_str_range* next_c_str_rangeref_arg) { 
  ((*next_c_str_rangeref_arg).c_str_range_idx = ((*next_c_str_rangeref_arg).c_str_range_idx + 1));
  return (*next_c_str_rangeref_arg).c_str_range_str[(*next_c_str_rangeref_arg).c_str_range_idx];
}

int main() { 
  c_str_range main_for3_target = iter_int8ptr("Hello");
  char main_idx = start_c_str_rangeref((&main_for3_target));
  for (;(false != stop_c_str_rangeref((&main_for3_target)));(main_idx = next_c_str_rangeref((&main_for3_target)))) {
printf("%c\n", main_idx);;
    }
  return 0;
}

