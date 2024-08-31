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
char _gc_running = false;
#include <stdarg.h>
#define c_va_start va_start
#define c_va_arg va_arg
void destruct_va_listref_1(va_list* destruct_va_listref_1_arg) { 
va_end((*destruct_va_listref_1_arg));
}
void* va_arg_va_list_voidptr_2(va_list va_arg_va_list_voidptr_2_list, void* va_arg_va_list_voidptr_2_argx) { 
  void* va_arg_va_list_voidptr_2_ret_27 = c_va_arg(va_arg_va_list_voidptr_2_list, void*);
  destruct_va_listref_1((&(va_arg_va_list_voidptr_2_list)));
  return va_arg_va_list_voidptr_2_ret_27;
}

long long va_arg_va_list_int64_2(va_list va_arg_va_list_int64_2_list, long long va_arg_va_list_int64_2_argx) { 
  long long va_arg_va_list_int64_2_ret_31 = (long long)c_va_arg(va_arg_va_list_int64_2_list, long long);
  destruct_va_listref_1((&(va_arg_va_list_int64_2_list)));
  return va_arg_va_list_int64_2_ret_31;
}

#include <sds.h>
sds copy_sdsref_1(sds* copy_sdsref_1_s) { 
  sds copy_sdsref_1_ret_18 = sdsdup((*copy_sdsref_1_s));
  return copy_sdsref_1_ret_18;
}

void destruct_sdsref_1(sds* destruct_sdsref_1_s) { 
sdsfree((*destruct_sdsref_1_s));
}
sds str_int8ptr_1(char* str_int8ptr_1_s) { 
  sds str_int8ptr_1_ret_28 = sdsnew(str_int8ptr_1_s);
  return str_int8ptr_1_ret_28;
}

sds str_sds_1(sds str_sds_1_s) { 
  sds str_sds_1_ret_32 = str_int8ptr_1((char*)str_sds_1_s);
  destruct_sdsref_1((&(str_sds_1_s)));
  return str_sds_1_ret_32;
}

sds str_from_int8ptr_1(char* str_from_int8ptr_1_fmt, ...) { 
  va_list str_from_int8ptr_1_listx;
  c_va_start(str_from_int8ptr_1_listx, (long long)str_from_int8ptr_1_fmt);
  sds str_from_int8ptr_1_tmp = sdsempty();
  sds str_from_int8ptr_1_ret_41 = sdscatvprintf(copy_sdsref_1((&(str_from_int8ptr_1_tmp))), str_from_int8ptr_1_fmt, str_from_int8ptr_1_listx);
  destruct_va_listref_1((&(str_from_int8ptr_1_listx)));
  destruct_sdsref_1((&(str_from_int8ptr_1_tmp)));
  return str_from_int8ptr_1_ret_41;
}

sds empty_str(void) { 
  sds empty_str_ret_47 = sdsempty();
  return empty_str_ret_47;
}

sds extend_sds_int64_2(sds extend_sds_int64_2_s, long long extend_sds_int64_2_size) { 
  sds extend_sds_int64_2_ret_54 = sdsgrowzero(copy_sdsref_1((&(extend_sds_int64_2_s))), extend_sds_int64_2_size);
  destruct_sdsref_1((&(extend_sds_int64_2_s)));
  return extend_sds_int64_2_ret_54;
}

sds copy_sds_1(sds copy_sds_1_s) { 
  sds copy_sds_1_ret_59 = sdsdup(copy_sds_1_s);
  destruct_sdsref_1((&(copy_sds_1_s)));
  return copy_sds_1_ret_59;
}

void clear_sdsref_1(sds* clear_sdsref_1_s) { 
  sdsclear((*clear_sdsref_1_s));
}
sds copy_sdsref_sdsref_2(sds* copy_sdsref_sdsref_2_s, sds* copy_sdsref_sdsref_2_t) { 
  sds copy_sdsref_sdsref_2_ret_73 = sdscpy(copy_sdsref_1(copy_sdsref_sdsref_2_s), (char*)(*copy_sdsref_sdsref_2_t));
  return copy_sdsref_sdsref_2_ret_73;
}

long long len_sds_1(sds len_sds_1_s) { 
  long long len_sds_1_ret_78 = sdslen(copy_sdsref_1((&(len_sds_1_s))));
  destruct_sdsref_1((&(len_sds_1_s)));
  return len_sds_1_ret_78;
}

sds substr_sdsref_int64_int64_3(sds* substr_sdsref_int64_int64_3_s, long long substr_sdsref_int64_int64_3_start, long long substr_sdsref_int64_int64_3_send) { 
  sds substr_sdsref_int64_int64_3_tmp = str_sds_1(copy_sdsref_1(substr_sdsref_int64_int64_3_s));
  sdsrange(copy_sdsref_1((&(substr_sdsref_int64_int64_3_tmp))), substr_sdsref_int64_int64_3_start, substr_sdsref_int64_int64_3_send);
  sds substr_sdsref_int64_int64_3_ret_99 = substr_sdsref_int64_int64_3_tmp;
  destruct_sdsref_1((&(substr_sdsref_int64_int64_3_tmp)));
  return substr_sdsref_int64_int64_3_ret_99;
}

sds concat_sdsref_sdsref_2(sds* concat_sdsref_sdsref_2_s, sds* concat_sdsref_sdsref_2_t) { 
  sds concat_sdsref_sdsref_2_tmp = str_sds_1(copy_sdsref_1(concat_sdsref_sdsref_2_s));
  sds concat_sdsref_sdsref_2_ret_110 = sdscatsds(copy_sdsref_1((&(concat_sdsref_sdsref_2_tmp))), copy_sdsref_1(concat_sdsref_sdsref_2_t));
  destruct_sdsref_1((&(concat_sdsref_sdsref_2_tmp)));
  return concat_sdsref_sdsref_2_ret_110;
}

sds concat_from_sdsref_int8ptr_2(sds* concat_from_sdsref_int8ptr_2_s, char* concat_from_sdsref_int8ptr_2_fmt, ...) { 
  va_list concat_from_sdsref_int8ptr_2_listx;
  c_va_start(concat_from_sdsref_int8ptr_2_listx, (long long)concat_from_sdsref_int8ptr_2_fmt);
  sds concat_from_sdsref_int8ptr_2_tmp = str_sds_1(copy_sdsref_1(concat_from_sdsref_int8ptr_2_s));
  sds concat_from_sdsref_int8ptr_2_ret_134 = sdscatvprintf(copy_sdsref_1((&(concat_from_sdsref_int8ptr_2_tmp))), concat_from_sdsref_int8ptr_2_fmt, concat_from_sdsref_int8ptr_2_listx);
  destruct_va_listref_1((&(concat_from_sdsref_int8ptr_2_listx)));
  destruct_sdsref_1((&(concat_from_sdsref_int8ptr_2_tmp)));
  return concat_from_sdsref_int8ptr_2_ret_134;
}

sds trim_sds_int8ptr_2(sds trim_sds_int8ptr_2_s, char* trim_sds_int8ptr_2_cset) { 
  sds trim_sds_int8ptr_2_tmp = str_sds_1(copy_sdsref_1((&(trim_sds_int8ptr_2_s))));
  sds trim_sds_int8ptr_2_ret_153 = sdstrim(copy_sdsref_1((&(trim_sds_int8ptr_2_tmp))), trim_sds_int8ptr_2_cset);
  destruct_sdsref_1((&(trim_sds_int8ptr_2_s)));
  destruct_sdsref_1((&(trim_sds_int8ptr_2_tmp)));
  return trim_sds_int8ptr_2_ret_153;
}

int compare_sdsref_sdsref_2(sds* compare_sdsref_sdsref_2_s, sds* compare_sdsref_sdsref_2_s2) { 
  int compare_sdsref_sdsref_2_ret_168 = sdscmp(copy_sdsref_1(compare_sdsref_sdsref_2_s), copy_sdsref_1(compare_sdsref_sdsref_2_s2));
  return compare_sdsref_sdsref_2_ret_168;
}

char equals_sds_sds_2(sds equals_sds_sds_2_s, sds equals_sds_sds_2_s2) { 
  char equals_sds_sds_2_ret_173 = ((long long)sdscmp(copy_sdsref_1((&(equals_sds_sds_2_s))), copy_sdsref_1((&(equals_sds_sds_2_s2)))) == 0);
  destruct_sdsref_1((&(equals_sds_sds_2_s)));
  destruct_sdsref_1((&(equals_sds_sds_2_s2)));
  return equals_sds_sds_2_ret_173;
}

char equals_sds_int8ptr_2(sds equals_sds_int8ptr_2_s, char* equals_sds_int8ptr_2_cs2) { 
  sds equals_sds_int8ptr_2_s2 = str_int8ptr_1(equals_sds_int8ptr_2_cs2);
  char equals_sds_int8ptr_2_ret_178 = ((long long)sdscmp(copy_sdsref_1((&(equals_sds_int8ptr_2_s))), copy_sdsref_1((&(equals_sds_int8ptr_2_s2)))) == 0);
  destruct_sdsref_1((&(equals_sds_int8ptr_2_s)));
  destruct_sdsref_1((&(equals_sds_int8ptr_2_s2)));
  return equals_sds_int8ptr_2_ret_178;
}

sds to_lower_sdsref_1(sds* to_lower_sdsref_1_s) { 
  sdstolower(copy_sdsref_1(to_lower_sdsref_1_s));
  sds to_lower_sdsref_1_ret_184 = (*to_lower_sdsref_1_s);
  return to_lower_sdsref_1_ret_184;
}

sds to_upper_sdsref_1(sds* to_upper_sdsref_1_s) { 
  sdstoupper(copy_sdsref_1(to_upper_sdsref_1_s));
  sds to_upper_sdsref_1_ret_190 = (*to_upper_sdsref_1_s);
  return to_upper_sdsref_1_ret_190;
}

long long find_sdsref_sdsref_2(sds* find_sdsref_sdsref_2_s, sds* find_sdsref_sdsref_2_sub) { 
  char* find_sdsref_sdsref_2_cs = (char*)(*find_sdsref_sdsref_2_s);
  char* find_sdsref_sdsref_2_ptr = strstr(find_sdsref_sdsref_2_cs, (char*)(*find_sdsref_sdsref_2_sub));
  long long find_sdsref_sdsref_2_ret_197 = ((find_sdsref_sdsref_2_ptr == (void*)0) ? (0 - 1) : ((long long)find_sdsref_sdsref_2_ptr - (long long)find_sdsref_sdsref_2_cs));
  return find_sdsref_sdsref_2_ret_197;
}

sds* split_int8ptr_int8ptr_int32ptr_3(char* split_int8ptr_int8ptr_int32ptr_3_cs, char* split_int8ptr_int8ptr_int32ptr_3_sep, int* split_int8ptr_int8ptr_int32ptr_3_cnt) { 
  sds* split_int8ptr_int8ptr_int32ptr_3_arr = sdssplitlen(split_int8ptr_int8ptr_int32ptr_3_cs, strlen(split_int8ptr_int8ptr_int32ptr_3_cs), split_int8ptr_int8ptr_int32ptr_3_sep, strlen(split_int8ptr_int8ptr_int32ptr_3_sep), split_int8ptr_int8ptr_int32ptr_3_cnt);
  if (split_int8ptr_int8ptr_int32ptr_3_arr == (void*)0) {
          printf("%s\n", "Cannot split string.");
    printf("Panicked in function %s, %s:%lld\n", "split_int8ptr_int8ptr_int32ptr_3", "../../include/stdlib/string.ml", 212);
    exit(1);
    }
  sds* split_int8ptr_int8ptr_int32ptr_3_ret_217 = split_int8ptr_int8ptr_int32ptr_3_arr;
  return split_int8ptr_int8ptr_int32ptr_3_ret_217;
}

sds* split_sds_sds_int32ptr_3(sds split_sds_sds_int32ptr_3_s, sds split_sds_sds_int32ptr_3_sep, int* split_sds_sds_int32ptr_3_cnt) { 
  sds* split_sds_sds_int32ptr_3_arr = sdssplitlen((char*)split_sds_sds_int32ptr_3_s, len_sds_1(copy_sdsref_1((&(split_sds_sds_int32ptr_3_s)))), (char*)split_sds_sds_int32ptr_3_sep, len_sds_1(copy_sdsref_1((&(split_sds_sds_int32ptr_3_sep)))), split_sds_sds_int32ptr_3_cnt);
  if (split_sds_sds_int32ptr_3_arr == (void*)0) {
          printf("%s\n", "Cannot split string.");
    printf("Panicked in function %s, %s:%lld\n", "split_sds_sds_int32ptr_3", "../../include/stdlib/string.ml", 224);
    exit(1);
    }
  sds* split_sds_sds_int32ptr_3_ret_229 = split_sds_sds_int32ptr_3_arr;
  destruct_sdsref_1((&(split_sds_sds_int32ptr_3_s)));
  destruct_sdsref_1((&(split_sds_sds_int32ptr_3_sep)));
  return split_sds_sds_int32ptr_3_ret_229;
}

sds* split_sds_int8ptr_int32ptr_3(sds split_sds_int8ptr_int32ptr_3_s, char* split_sds_int8ptr_int32ptr_3_sep, int* split_sds_int8ptr_int32ptr_3_cnt) { 
  sds* split_sds_int8ptr_int32ptr_3_arr = sdssplitlen((char*)split_sds_int8ptr_int32ptr_3_s, len_sds_1(copy_sdsref_1((&(split_sds_int8ptr_int32ptr_3_s)))), split_sds_int8ptr_int32ptr_3_sep, strlen(split_sds_int8ptr_int32ptr_3_sep), split_sds_int8ptr_int32ptr_3_cnt);
  if (split_sds_int8ptr_int32ptr_3_arr == (void*)0) {
          printf("%s\n", "Cannot split string.");
    printf("Panicked in function %s, %s:%lld\n", "split_sds_int8ptr_int32ptr_3", "../../include/stdlib/string.ml", 236);
    exit(1);
    }
  sds* split_sds_int8ptr_int32ptr_3_ret_241 = split_sds_int8ptr_int32ptr_3_arr;
  destruct_sdsref_1((&(split_sds_int8ptr_int32ptr_3_s)));
  return split_sds_int8ptr_int32ptr_3_ret_241;
}

sds join_voidptr_int32_int8ptr_3(void* join_voidptr_int32_int8ptr_3_argv, int join_voidptr_int32_int8ptr_3_argc, char* join_voidptr_int32_int8ptr_3_sep) { 
  sds join_voidptr_int32_int8ptr_3_ret_247 = sdsjoin(join_voidptr_int32_int8ptr_3_argv, join_voidptr_int32_int8ptr_3_argc, join_voidptr_int32_int8ptr_3_sep);
  return join_voidptr_int32_int8ptr_3_ret_247;
}

sds to_str_bool_1(char to_str_bool_1_value) { 
  if (to_str_bool_1_value == true) {
          sds to_str_bool_1_ret_253 = str_int8ptr_1("true");
    return to_str_bool_1_ret_253;
    }
  else {
     sds to_str_bool_1_ret_255 = str_int8ptr_1("false");
  return to_str_bool_1_ret_255;
    }
}

sds to_str_int64_1(long long to_str_int64_1_value) { 
  sds to_str_int64_1_ret_262 = sdsfromlonglong(to_str_int64_1_value);
  return to_str_int64_1_ret_262;
}

sds to_str_sdsref_1(sds* to_str_sdsref_1_value) { 
  sds to_str_sdsref_1_ret_267 = copy_sds_1(copy_sdsref_1(to_str_sdsref_1_value));
  return to_str_sdsref_1_ret_267;
}

sds to_str_int8ptr_1(char* to_str_int8ptr_1_value) { 
  sds to_str_int8ptr_1_ret_272 = str_int8ptr_1(to_str_int8ptr_1_value);
  return to_str_int8ptr_1_ret_272;
}

sds to_str_voidptr_1(void* to_str_voidptr_1_value) { 
  sds to_str_voidptr_1_ret_277 = str_from_int8ptr_1("%p", to_str_voidptr_1_value);
  return to_str_voidptr_1_ret_277;
}

FILE* open_file_int8ptr_int8ptr_2(char* open_file_int8ptr_int8ptr_2_filename, char* open_file_int8ptr_int8ptr_2_mode) { 
  void* open_file_int8ptr_int8ptr_2_st = fopen(open_file_int8ptr_int8ptr_2_filename, open_file_int8ptr_int8ptr_2_mode);
  if (open_file_int8ptr_int8ptr_2_st == (void*)0) {
          printf("No such file '%s'", open_file_int8ptr_int8ptr_2_filename);
    printf("\n");
    printf("Panicked in function %s, %s:%lld\n", "open_file_int8ptr_int8ptr_2", "../../include/stdlib/io/file.ml", 32);
    exit(1);
    }
  void* open_file_int8ptr_int8ptr_2_ret_37 = open_file_int8ptr_int8ptr_2_st;
  return open_file_int8ptr_int8ptr_2_ret_37;
}

FILE* open_file_int8ptr_1(char* open_file_int8ptr_1_filename) { 
  FILE* open_file_int8ptr_1_ret_42 = open_file_int8ptr_int8ptr_2(open_file_int8ptr_1_filename, "r");
  return open_file_int8ptr_1_ret_42;
}

char read_line_FILEptr_sds_int64_3(FILE* read_line_FILEptr_sds_int64_3_st, sds read_line_FILEptr_sds_int64_3_s, long long read_line_FILEptr_sds_int64_3_size) { 
  char* read_line_FILEptr_sds_int64_3_ln = fgets((char*)read_line_FILEptr_sds_int64_3_s, read_line_FILEptr_sds_int64_3_size, read_line_FILEptr_sds_int64_3_st);
  char read_line_FILEptr_sds_int64_3_ret_48 = (read_line_FILEptr_sds_int64_3_ln != (void*)0);
  destruct_sdsref_1((&(read_line_FILEptr_sds_int64_3_s)));
  return read_line_FILEptr_sds_int64_3_ret_48;
}

sds read_file_FILEptr_int64_2(FILE* read_file_FILEptr_int64_2_st, long long read_file_FILEptr_int64_2_size) { 
  sds read_file_FILEptr_int64_2_s = empty_str();
  char* read_file_FILEptr_int64_2_cs = malloc(read_file_FILEptr_int64_2_size);
  fread(read_file_FILEptr_int64_2_cs, read_file_FILEptr_int64_2_size, 1, read_file_FILEptr_int64_2_st);
  (read_file_FILEptr_int64_2_cs[read_file_FILEptr_int64_2_size] = 0);
  sds read_file_FILEptr_int64_2_ret_60 = read_file_FILEptr_int64_2_s;
  destruct_sdsref_1((&(read_file_FILEptr_int64_2_s)));
  return read_file_FILEptr_int64_2_ret_60;
  (read_file_FILEptr_int64_2_s = str_int8ptr_1(read_file_FILEptr_int64_2_cs));
  free(read_file_FILEptr_int64_2_cs);
}

sds read_file_FILEptr_1(FILE* read_file_FILEptr_1_st) { 
  fseek(read_file_FILEptr_1_st, 0, (int)SEEK_END);
  long long read_file_FILEptr_1_size = ftell(read_file_FILEptr_1_st);
  rewind(read_file_FILEptr_1_st);
  sds read_file_FILEptr_1_ret_71 = read_file_FILEptr_int64_2(read_file_FILEptr_1_st, read_file_FILEptr_1_size);
  return read_file_FILEptr_1_ret_71;
}

typedef struct {
 long long range_elem_range_idx;
long long range_elem_range_start;
long long range_elem_range_stop;;
} range;

range range_int64_int64_int64_3(long long range_elem_range_idx, long long range_elem_range_start, long long range_elem_range_stop) { 
  range range_tmp;
  (range_tmp.range_elem_range_idx = range_elem_range_idx);
  (range_tmp.range_elem_range_start = range_elem_range_start);
  (range_tmp.range_elem_range_stop = range_elem_range_stop);
  return range_tmp;
}
range range_int64_int64_2(long long range_int64_int64_2_range_start, long long range_int64_int64_2_range_stop) { 
  range range_int64_int64_2_ret_13 = range_int64_int64_int64_3(0, range_int64_int64_2_range_start, range_int64_int64_2_range_stop);
  return range_int64_int64_2_ret_13;
}

range range_int64_1(long long range_int64_1_range_stop) { 
  range range_int64_1_ret_17 = range_int64_int64_int64_3(0, 0, range_int64_1_range_stop);
  return range_int64_1_ret_17;
}

range iter_rangeref_1(range* iter_rangeref_1_arg) { 
  range iter_rangeref_1_ret_21 = (*iter_rangeref_1_arg);
  return iter_rangeref_1_ret_21;
}

long long start_rangeref_1(range* start_rangeref_1_arg) { 
  long long start_rangeref_1_ret_25 = start_rangeref_1_arg->range_elem_range_start;
  return start_rangeref_1_ret_25;
}

char stop_rangeref_1(range* stop_rangeref_1_arg) { 
  char stop_rangeref_1_ret_29 = (stop_rangeref_1_arg->range_elem_range_idx < stop_rangeref_1_arg->range_elem_range_stop);
  return stop_rangeref_1_ret_29;
}

long long next_rangeref_1(range* next_rangeref_1_arg) { 
  (next_rangeref_1_arg->range_elem_range_idx = (next_rangeref_1_arg->range_elem_range_idx + 1));
  long long next_rangeref_1_ret_34 = next_rangeref_1_arg->range_elem_range_idx;
  return next_rangeref_1_ret_34;
}

typedef struct {
 FILE* file_range_elem_file_range_st;
char* file_range_elem_file_range_str;
char file_range_elem_file_range_succ;;
} file_range;

file_range file_range_FILEptr_int8ptr_bool_3(FILE* file_range_elem_file_range_st, char* file_range_elem_file_range_str, char file_range_elem_file_range_succ) { 
  file_range file_range_tmp;
  (file_range_tmp.file_range_elem_file_range_st = file_range_elem_file_range_st);
  (file_range_tmp.file_range_elem_file_range_str = file_range_elem_file_range_str);
  (file_range_tmp.file_range_elem_file_range_succ = file_range_elem_file_range_succ);
  return file_range_tmp;
}
file_range lines_FILEptr_1(FILE* lines_FILEptr_1_arg) { 
  sds lines_FILEptr_1_s = empty_str();
  (lines_FILEptr_1_s = extend_sds_int64_2(copy_sdsref_1((&(lines_FILEptr_1_s))), 256));
  char lines_FILEptr_1_succ = read_line_FILEptr_sds_int64_3(lines_FILEptr_1_arg, copy_sdsref_1((&(lines_FILEptr_1_s))), 256);
  file_range lines_FILEptr_1_ret_49 = file_range_FILEptr_int8ptr_bool_3(lines_FILEptr_1_arg, (char*)lines_FILEptr_1_s, lines_FILEptr_1_succ);
  destruct_sdsref_1((&(lines_FILEptr_1_s)));
  return lines_FILEptr_1_ret_49;
}

file_range iter_file_rangeref_1(file_range* iter_file_rangeref_1_arg) { 
  file_range iter_file_rangeref_1_ret_53 = (*iter_file_rangeref_1_arg);
  return iter_file_rangeref_1_ret_53;
}

sds next_file_rangeref_1(file_range* next_file_rangeref_1_arg) { 
  sds next_file_rangeref_1_s = empty_str();
  (next_file_rangeref_1_s = extend_sds_int64_2(copy_sdsref_1((&(next_file_rangeref_1_s))), 256));
  char next_file_rangeref_1_succ = read_line_FILEptr_sds_int64_3(next_file_rangeref_1_arg->file_range_elem_file_range_st, copy_sdsref_1((&(next_file_rangeref_1_s))), 256);
  (next_file_rangeref_1_arg->file_range_elem_file_range_str = (char*)next_file_rangeref_1_s);
  (next_file_rangeref_1_arg->file_range_elem_file_range_succ = next_file_rangeref_1_succ);
  sds next_file_rangeref_1_ret_64 = next_file_rangeref_1_s;
  destruct_sdsref_1((&(next_file_rangeref_1_s)));
  return next_file_rangeref_1_ret_64;
}

sds start_file_rangeref_1(file_range* start_file_rangeref_1_arg) { 
  if (start_file_rangeref_1_arg->file_range_elem_file_range_succ == false) {
          printf("%s\n", "Attempt to read from empty file");
    printf("Panicked in function %s, %s:%lld\n", "start_file_rangeref_1", "../../include/stdlib/builtin/for.ml", 69);
    exit(1);
    }
  sds start_file_rangeref_1_s = str_int8ptr_1(start_file_rangeref_1_arg->file_range_elem_file_range_str);
  next_file_rangeref_1(start_file_rangeref_1_arg);
  sds start_file_rangeref_1_ret_77 = start_file_rangeref_1_s;
  destruct_sdsref_1((&(start_file_rangeref_1_s)));
  return start_file_rangeref_1_ret_77;
}

char stop_file_rangeref_1(file_range* stop_file_rangeref_1_arg) { 
  char stop_file_rangeref_1_ret_81 = (stop_file_rangeref_1_arg->file_range_elem_file_range_succ == true);
  return stop_file_rangeref_1_ret_81;
}

typedef struct {
 char* c_str_range_elem_c_str_range_str;
long long c_str_range_elem_c_str_range_idx;
long long c_str_range_elem_c_str_range_start;
long long c_str_range_elem_c_str_range_stop;;
} c_str_range;

c_str_range c_str_range_int8ptr_int64_int64_int64_4(char* c_str_range_elem_c_str_range_str, long long c_str_range_elem_c_str_range_idx, long long c_str_range_elem_c_str_range_start, long long c_str_range_elem_c_str_range_stop) { 
  c_str_range c_str_range_tmp;
  (c_str_range_tmp.c_str_range_elem_c_str_range_str = c_str_range_elem_c_str_range_str);
  (c_str_range_tmp.c_str_range_elem_c_str_range_idx = c_str_range_elem_c_str_range_idx);
  (c_str_range_tmp.c_str_range_elem_c_str_range_start = c_str_range_elem_c_str_range_start);
  (c_str_range_tmp.c_str_range_elem_c_str_range_stop = c_str_range_elem_c_str_range_stop);
  return c_str_range_tmp;
}
c_str_range iter_sdsref_1(sds* iter_sdsref_1_arg) { 
  c_str_range iter_sdsref_1_ret_93 = c_str_range_int8ptr_int64_int64_int64_4((char*)(*iter_sdsref_1_arg), 0, 0, len_sds_1(copy_sdsref_1(iter_sdsref_1_arg)));
  return iter_sdsref_1_ret_93;
}

c_str_range iter_int8ptr_1(char* iter_int8ptr_1_arg) { 
  c_str_range iter_int8ptr_1_ret_97 = c_str_range_int8ptr_int64_int64_int64_4(iter_int8ptr_1_arg, 0, 0, strlen(iter_int8ptr_1_arg));
  return iter_int8ptr_1_ret_97;
}

char start_c_str_rangeref_1(c_str_range* start_c_str_rangeref_1_arg) { 
  char start_c_str_rangeref_1_ret_101 = start_c_str_rangeref_1_arg->c_str_range_elem_c_str_range_str[start_c_str_rangeref_1_arg->c_str_range_elem_c_str_range_start];
  return start_c_str_rangeref_1_ret_101;
}

char stop_c_str_rangeref_1(c_str_range* stop_c_str_rangeref_1_arg) { 
  char stop_c_str_rangeref_1_ret_105 = (stop_c_str_rangeref_1_arg->c_str_range_elem_c_str_range_idx < stop_c_str_rangeref_1_arg->c_str_range_elem_c_str_range_stop);
  return stop_c_str_rangeref_1_ret_105;
}

char next_c_str_rangeref_1(c_str_range* next_c_str_rangeref_1_arg) { 
  (next_c_str_rangeref_1_arg->c_str_range_elem_c_str_range_idx = (next_c_str_rangeref_1_arg->c_str_range_elem_c_str_range_idx + 1));
  char next_c_str_rangeref_1_ret_110 = next_c_str_rangeref_1_arg->c_str_range_elem_c_str_range_str[next_c_str_rangeref_1_arg->c_str_range_elem_c_str_range_idx];
  return next_c_str_rangeref_1_ret_110;
}

typedef struct {
 long long str_list_elem_str_list_cnt;
sds* str_list_elem_str_list_arr;;
} str_list;

str_list str_list_int64_sdsptr_2(long long str_list_elem_str_list_cnt, sds* str_list_elem_str_list_arr) { 
  str_list str_list_tmp;
  (str_list_tmp.str_list_elem_str_list_cnt = str_list_elem_str_list_cnt);
  (str_list_tmp.str_list_elem_str_list_arr = str_list_elem_str_list_arr);
  return str_list_tmp;
}
str_list _str_listv_int64_va_list_2(long long _str_listv_int64_va_list_2_cnt, va_list _str_listv_int64_va_list_2_listx) { 
  sds* _str_listv_int64_va_list_2_arr = (void*)0;
  if (_gc_running == true) {
      (_str_listv_int64_va_list_2_arr = ml_malloc((_str_listv_int64_va_list_2_cnt * 8)));
    }
  else {
     (_str_listv_int64_va_list_2_arr = malloc((_str_listv_int64_va_list_2_cnt * 8)));
  printf("Allocation defaults to malloc in %s:%s. Consider starting the gc by using alloc_start.\n", "_str_listv_int64_va_list_2", "../../include/stdlib/str_list.ml");
    }
  if (_str_listv_int64_va_list_2_arr == (void*)0) {
          printf("%s\n", "Allocation failed.");
    printf("Panicked in function %s, %s:%lld\n", "_str_listv_int64_va_list_2", "../../include/stdlib/str_list.ml", 24);
    exit(1);
    }
  range _str_listv_int64_va_list_2_r = range_int64_1(_str_listv_int64_va_list_2_cnt);
  range _str_listv_int64_va_list_2_for31_target = iter_rangeref_1((&(_str_listv_int64_va_list_2_r)));
  long long _str_listv_int64_va_list_2_it = start_rangeref_1((&(_str_listv_int64_va_list_2_for31_target)));
  for (;(false != stop_rangeref_1((&(_str_listv_int64_va_list_2_for31_target))));(_str_listv_int64_va_list_2_it = next_rangeref_1((&(_str_listv_int64_va_list_2_for31_target))))) {
  char* _str_listv_int64_va_list_2_arg = c_va_arg(_str_listv_int64_va_list_2_listx, void*);
  (_str_listv_int64_va_list_2_arr[_str_listv_int64_va_list_2_it] = str_int8ptr_1(_str_listv_int64_va_list_2_arg));;;
    }
  str_list _str_listv_int64_va_list_2_ret_36 = str_list_int64_sdsptr_2(_str_listv_int64_va_list_2_cnt, _str_listv_int64_va_list_2_arr);
  destruct_va_listref_1((&(_str_listv_int64_va_list_2_listx)));
  return _str_listv_int64_va_list_2_ret_36;
}

str_list _str_list_int64_1(long long _str_list_int64_1_cnt, ...) { 
  va_list _str_list_int64_1_listx;
  c_va_start(_str_list_int64_1_listx, (long long)_str_list_int64_1_cnt);
  str_list _str_list_int64_1_ret_43 = _str_listv_int64_va_list_2(_str_list_int64_1_cnt, _str_list_int64_1_listx);
  destruct_va_listref_1((&(_str_list_int64_1_listx)));
  return _str_list_int64_1_ret_43;
}

str_list str_list_int64_va_list_2(long long str_list_int64_va_list_2_cnt, va_list str_list_int64_va_list_2_listx) { 
  str_list str_list_int64_va_list_2_ret_47 = _str_listv_int64_va_list_2(str_list_int64_va_list_2_cnt, str_list_int64_va_list_2_listx);
  destruct_va_listref_1((&(str_list_int64_va_list_2_listx)));
  return str_list_int64_va_list_2_ret_47;
}

typedef struct {
 long long str_list_range_elem_str_list_range_idx;
long long str_list_range_elem_str_list_range_cnt;
sds* str_list_range_elem_str_list_range_arr;;
} str_list_range;

str_list_range str_list_range_int64_int64_sdsptr_3(long long str_list_range_elem_str_list_range_idx, long long str_list_range_elem_str_list_range_cnt, sds* str_list_range_elem_str_list_range_arr) { 
  str_list_range str_list_range_tmp;
  (str_list_range_tmp.str_list_range_elem_str_list_range_idx = str_list_range_elem_str_list_range_idx);
  (str_list_range_tmp.str_list_range_elem_str_list_range_cnt = str_list_range_elem_str_list_range_cnt);
  (str_list_range_tmp.str_list_range_elem_str_list_range_arr = str_list_range_elem_str_list_range_arr);
  return str_list_range_tmp;
}
str_list_range iter_str_listref_1(str_list* iter_str_listref_1_arg) { 
  str_list_range iter_str_listref_1_ret_63 = str_list_range_int64_int64_sdsptr_3(0, iter_str_listref_1_arg->str_list_elem_str_list_cnt, iter_str_listref_1_arg->str_list_elem_str_list_arr);
  return iter_str_listref_1_ret_63;
}

sds start_str_list_rangeref_1(str_list_range* start_str_list_rangeref_1_arg) { 
  sds start_str_list_rangeref_1_ret_67 = start_str_list_rangeref_1_arg->str_list_range_elem_str_list_range_arr[start_str_list_rangeref_1_arg->str_list_range_elem_str_list_range_idx];
  return start_str_list_rangeref_1_ret_67;
}

char stop_str_list_rangeref_1(str_list_range* stop_str_list_rangeref_1_arg) { 
  char stop_str_list_rangeref_1_ret_71 = (stop_str_list_rangeref_1_arg->str_list_range_elem_str_list_range_idx < stop_str_list_rangeref_1_arg->str_list_range_elem_str_list_range_cnt);
  return stop_str_list_rangeref_1_ret_71;
}

sds next_str_list_rangeref_1(str_list_range* next_str_list_rangeref_1_arg) { 
  (next_str_list_rangeref_1_arg->str_list_range_elem_str_list_range_idx = (next_str_list_rangeref_1_arg->str_list_range_elem_str_list_range_idx + 1));
  if (stop_str_list_rangeref_1(next_str_list_rangeref_1_arg) == true) {
          sds next_str_list_rangeref_1_ret_77 = next_str_list_rangeref_1_arg->str_list_range_elem_str_list_range_arr[next_str_list_rangeref_1_arg->str_list_range_elem_str_list_range_idx];
    return next_str_list_rangeref_1_ret_77;
    }
  else {
     sds next_str_list_rangeref_1_ret_79 = empty_str();
  return next_str_list_rangeref_1_ret_79;
    }
}

sds input(void) { 
  long long input_size = 128;
  long long input_length = 0;
  int input_ch = 1;
  char* input_buff = malloc(input_size);
  if (input_buff == (void*)0) {
          printf("%s\n", "Unable to allocate buff");
    printf("Panicked in function %s, %s:%lld\n", "input", "../../include/stdlib/io/read.ml", 17);
    exit(1);
    }
  while ((input_ch = getchar()) != (long long)'\n') {
    if ((input_length + 1) >= input_size) {
              (input_size = (input_size * 2));
      (input_buff = realloc(input_buff, input_size));
      if (input_buff == (void*)0) {
                  printf("%s\n", "Unable to reallocate buff");
        printf("Panicked in function %s, %s:%lld\n", "input", "../../include/stdlib/io/read.ml", 28);
        exit(1);
            }
        }
    (input_buff[input_length] = input_ch);
    (input_length = (input_length + 1));;
    }
  (input_buff[input_length] = 0);
  sds input_s = str_int8ptr_1(input_buff);
  sds input_ret_40 = input_s;
  destruct_sdsref_1((&(input_s)));
  return input_ret_40;
  free(input_buff);
}

void _read_FILEptr_int8ptr_2(FILE* _read_FILEptr_int8ptr_2_st, char* _read_FILEptr_int8ptr_2_arg) { 
  fscanf(_read_FILEptr_int8ptr_2_st, "%hhd", _read_FILEptr_int8ptr_2_arg);
}
void _read_FILEptr_int16ptr_2(FILE* _read_FILEptr_int16ptr_2_st, short* _read_FILEptr_int16ptr_2_arg) { 
  fscanf(_read_FILEptr_int16ptr_2_st, "%hd", _read_FILEptr_int16ptr_2_arg);
}
void _read_FILEptr_int32ptr_2(FILE* _read_FILEptr_int32ptr_2_st, int* _read_FILEptr_int32ptr_2_arg) { 
  fscanf(_read_FILEptr_int32ptr_2_st, "%d", _read_FILEptr_int32ptr_2_arg);
}
void _read_FILEptr_int64ptr_2(FILE* _read_FILEptr_int64ptr_2_st, long long* _read_FILEptr_int64ptr_2_arg) { 
  fscanf(_read_FILEptr_int64ptr_2_st, "%Ld", _read_FILEptr_int64ptr_2_arg);
}
void _read_FILEptr_voidptr_2(FILE* _read_FILEptr_voidptr_2_st, void* _read_FILEptr_voidptr_2_arg) { 
  printf("%s\n", "Cannot read void value");
  printf("Panicked in function %s, %s:%lld\n", "_read_FILEptr_voidptr_2", "../../include/stdlib/io/read.ml", 57);
  exit(1);
}
void _read_FILEptr_boolptr_2(FILE* _read_FILEptr_boolptr_2_st, char* _read_FILEptr_boolptr_2_arg) { 
  printf("%s\n", "Cannot read boolean value");
  printf("Panicked in function %s, %s:%lld\n", "_read_FILEptr_boolptr_2", "../../include/stdlib/io/read.ml", 62);
  exit(1);
}
void _print_FILEptr_int64_2(FILE* _print_FILEptr_int64_2_st, long long _print_FILEptr_int64_2_arg) { 
  fprintf(_print_FILEptr_int64_2_st, "%lld", _print_FILEptr_int64_2_arg);
}
void _print_FILEptr_int32_2(FILE* _print_FILEptr_int32_2_st, int _print_FILEptr_int32_2_arg) { 
  fprintf(_print_FILEptr_int32_2_st, "%d", _print_FILEptr_int32_2_arg);
}
void _print_FILEptr_int16_2(FILE* _print_FILEptr_int16_2_st, short _print_FILEptr_int16_2_arg) { 
  fprintf(_print_FILEptr_int16_2_st, "%hd", _print_FILEptr_int16_2_arg);
}
void _print_FILEptr_int8_2(FILE* _print_FILEptr_int8_2_st, char _print_FILEptr_int8_2_arg) { 
  fprintf(_print_FILEptr_int8_2_st, "%hhd", _print_FILEptr_int8_2_arg);
}
void _print_FILEptr_sds_2(FILE* _print_FILEptr_sds_2_st, sds _print_FILEptr_sds_2_arg) { 
  fprintf(_print_FILEptr_sds_2_st, "%s", (char*)_print_FILEptr_sds_2_arg);
destruct_sdsref_1((&(_print_FILEptr_sds_2_arg)));
}
void _print_FILEptr_sdsref_2(FILE* _print_FILEptr_sdsref_2_st, sds* _print_FILEptr_sdsref_2_arg) { 
  fprintf(_print_FILEptr_sdsref_2_st, "%s", (char*)(*_print_FILEptr_sdsref_2_arg));
}
void _print_FILEptr_voidptr_2(FILE* _print_FILEptr_voidptr_2_st, void* _print_FILEptr_voidptr_2_arg) { 
  fprintf(_print_FILEptr_voidptr_2_st, "%p", _print_FILEptr_voidptr_2_arg);
}
void _print_FILEptr_int8ptr_2(FILE* _print_FILEptr_int8ptr_2_st, char* _print_FILEptr_int8ptr_2_arg) { 
  fprintf(_print_FILEptr_int8ptr_2_st, "%s", _print_FILEptr_int8ptr_2_arg);
}
void _print_FILEptr_bool_2(FILE* _print_FILEptr_bool_2_st, char _print_FILEptr_bool_2_arg) { 
  if (_print_FILEptr_bool_2_arg == true) {
      fprintf(_print_FILEptr_bool_2_st, "true");
    }
  else if (_print_FILEptr_bool_2_arg == false) {
   fprintf(_print_FILEptr_bool_2_st, "false");
    }
  else {
     printf("%s\n", "Logic error");
  printf("Panicked in function %s, %s:%lld\n", "_print_FILEptr_bool_2", "../../include/stdlib/io/print.ml", 39);
  exit(1);
    }
}
typedef struct {
 long long _tok_type_elem_err;
long long _tok_type_elem_num;
long long _tok_type_elem_add;
long long _tok_type_elem_sub;
long long _tok_type_elem_div;
long long _tok_type_elem_mult;;
} _tok_type;

_tok_type _tok_type_int64_int64_int64_int64_int64_int64_6(long long _tok_type_elem_err, long long _tok_type_elem_num, long long _tok_type_elem_add, long long _tok_type_elem_sub, long long _tok_type_elem_div, long long _tok_type_elem_mult) { 
  _tok_type _tok_type_tmp;
  (_tok_type_tmp._tok_type_elem_err = _tok_type_elem_err);
  (_tok_type_tmp._tok_type_elem_num = _tok_type_elem_num);
  (_tok_type_tmp._tok_type_elem_add = _tok_type_elem_add);
  (_tok_type_tmp._tok_type_elem_sub = _tok_type_elem_sub);
  (_tok_type_tmp._tok_type_elem_div = _tok_type_elem_div);
  (_tok_type_tmp._tok_type_elem_mult = _tok_type_elem_mult);
  return _tok_type_tmp;
}
typedef struct {
 long long tok_elem_type;
char* tok_elem_value;;
} tok;

tok tok_int64_int8ptr_2(long long tok_elem_type, char* tok_elem_value) { 
  tok tok_tmp;
  (tok_tmp.tok_elem_type = tok_elem_type);
  (tok_tmp.tok_elem_value = tok_elem_value);
  return tok_tmp;
}
sds rev_tok_type_of_int64_1(long long rev_tok_type_of_int64_1_type) { 
  char* rev_tok_type_of_int64_1_cs = (void*)0;
  if (rev_tok_type_of_int64_1_type == _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_err) {
      (rev_tok_type_of_int64_1_cs = "err");
    }
  else if (rev_tok_type_of_int64_1_type == _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_num) {
   (rev_tok_type_of_int64_1_cs = "num");
    }
  else if (rev_tok_type_of_int64_1_type == _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_add) {
   (rev_tok_type_of_int64_1_cs = "+");
    }
  else if (rev_tok_type_of_int64_1_type == _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_sub) {
   (rev_tok_type_of_int64_1_cs = "-");
    }
  else if (rev_tok_type_of_int64_1_type == _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_div) {
   (rev_tok_type_of_int64_1_cs = "/");
    }
  else if (rev_tok_type_of_int64_1_type == _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_mult) {
   (rev_tok_type_of_int64_1_cs = "*");
    }
  else {
     printf("%s\n", "Invalid token type");
  printf("Panicked in function %s, %s:%lld\n", "rev_tok_type_of_int64_1", "src/main.ml", 44);
  exit(1);
    }
  sds rev_tok_type_of_int64_1_ret_49 = str_int8ptr_1(rev_tok_type_of_int64_1_cs);
  return rev_tok_type_of_int64_1_ret_49;
}

void _print_FILEptr_tokref_2(FILE* _print_FILEptr_tokref_2_cs, tok* _print_FILEptr_tokref_2_arg) { 
  sds _print_FILEptr_tokref_2_rev = rev_tok_type_of_int64_1(_print_FILEptr_tokref_2_arg->tok_elem_type);
  _print_FILEptr_int8ptr_2((FILE*)stdout, "tok(type = ");
  _print_FILEptr_sdsref_2((FILE*)stdout, (&(_print_FILEptr_tokref_2_rev)));
  _print_FILEptr_int8ptr_2((FILE*)stdout, ", value = ");
  _print_FILEptr_int8ptr_2((FILE*)stdout, _print_FILEptr_tokref_2_arg->tok_elem_value);
  _print_FILEptr_int8ptr_2((FILE*)stdout, ")");
}
char is_num_sdsref_1(sds* is_num_sdsref_1_s) { 
  c_str_range is_num_sdsref_1_for62_target = iter_sdsref_1(is_num_sdsref_1_s);
  char is_num_sdsref_1_ch = start_c_str_rangeref_1((&(is_num_sdsref_1_for62_target)));
  for (;(false != stop_c_str_rangeref_1((&(is_num_sdsref_1_for62_target))));(is_num_sdsref_1_ch = next_c_str_rangeref_1((&(is_num_sdsref_1_for62_target))))) {
  if ((long long)isdigit(is_num_sdsref_1_ch) == 0) {
          char is_num_sdsref_1_ret_64 = false;
    return is_num_sdsref_1_ret_64;
    };;
    }
  char is_num_sdsref_1_ret_68 = true;
  return is_num_sdsref_1_ret_68;
}

long long tok_type_of_sdsref_1(sds* tok_type_of_sdsref_1_s) { 
  if (is_num_sdsref_1(tok_type_of_sdsref_1_s) == true) {
          long long tok_type_of_sdsref_1_ret_74 = _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_num;
    return tok_type_of_sdsref_1_ret_74;
    }
  else if (equals_sds_int8ptr_2((*tok_type_of_sdsref_1_s), "+") == true) {
     long long tok_type_of_sdsref_1_ret_77 = _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_add;
  return tok_type_of_sdsref_1_ret_77;
    }
  else if (equals_sds_int8ptr_2((*tok_type_of_sdsref_1_s), "-") == true) {
     long long tok_type_of_sdsref_1_ret_80 = _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_sub;
  return tok_type_of_sdsref_1_ret_80;
    }
  else if (equals_sds_int8ptr_2((*tok_type_of_sdsref_1_s), "/") == true) {
     long long tok_type_of_sdsref_1_ret_83 = _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_div;
  return tok_type_of_sdsref_1_ret_83;
    }
  else if (equals_sds_int8ptr_2((*tok_type_of_sdsref_1_s), "*") == true) {
     long long tok_type_of_sdsref_1_ret_86 = _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_mult;
  return tok_type_of_sdsref_1_ret_86;
    }
  long long tok_type_of_sdsref_1_ret_90 = _tok_type_int64_int64_int64_int64_int64_int64_6(0, 1, 2, 3, 4, 5)._tok_type_elem_err;
  return tok_type_of_sdsref_1_ret_90;
}

tok tok_sdsref_1(sds* tok_sdsref_1_value) { 
  tok tok_sdsref_1_ret_94 = tok_int64_int8ptr_2(tok_type_of_sdsref_1(tok_sdsref_1_value), (char*)(*tok_sdsref_1_value));
  return tok_sdsref_1_ret_94;
}

void lex_sdsref_1(sds* lex_sdsref_1_ln) { 
  int lex_sdsref_1_cnt = 0;
  sds* lex_sdsref_1_arr = split_sds_int8ptr_int32ptr_3(trim_sds_int8ptr_2((*lex_sdsref_1_ln), "\n"), " ", (&(lex_sdsref_1_cnt)));
  str_list lex_sdsref_1_list = str_list_int64_sdsptr_2(lex_sdsref_1_cnt, lex_sdsref_1_arr);
  str_list_range lex_sdsref_1_for102_target = iter_str_listref_1((&(lex_sdsref_1_list)));
  sds lex_sdsref_1_it = start_str_list_rangeref_1((&(lex_sdsref_1_for102_target)));
  for (;(false != stop_str_list_rangeref_1((&(lex_sdsref_1_for102_target))));(lex_sdsref_1_it = next_str_list_rangeref_1((&(lex_sdsref_1_for102_target))))) {
  tok lex_sdsref_1_tk = tok_sdsref_1((&(lex_sdsref_1_it)));
  _print_FILEptr_tokref_2((FILE*)stdout, (&(lex_sdsref_1_tk)));
  puts("");;;
    }
}
int main(void) { 
  long long main_bos = 0;
  if (_gc_running == true) {
          printf("%s\n", "Cannot start an already running gc.");
    printf("Panicked in function %s, %s:%lld\n", "main", "src/main.ml", 113);
    exit(1);
    }
  #undef s_malloc
  #undef s_realloc
  #undef s_free
  #define s_malloc ml_malloc
  #define s_realloc ml_realloc
  #define s_free ml_free
  gc_start((&(ml_gc)), (&(main_bos)));
  (_gc_running = true);
  sds main_s = input();
  lex_sdsref_1((&(main_s)));
  long long main_ret_147 = 0;
  destruct_sdsref_1((&(main_s)));
  return main_ret_147;
  if (_gc_running == false) {
          printf("%s\n", "Cannot stop an already stopped gc.");
    printf("Panicked in function %s, %s:%lld\n", "main", "src/main.ml", 127);
    exit(1);
    }
  #undef s_malloc
  #undef s_realloc
  #undef s_free
  #define s_malloc malloc
  #define s_realloc realloc
  #define s_free free
  gc_stop((&(ml_gc)));
  (_gc_running = false);
}

