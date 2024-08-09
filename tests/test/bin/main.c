#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

void _print_bool(char _print_bool_arg) { 
  if (_print_bool_arg == true) {
      printf("true");
    }
  else {
   printf("false");
    }
}

void _print_int8(char _print_int8_arg) { 
  printf("%hhd", _print_int8_arg);
}

void _print_int16(short _print_int16_arg) { 
  printf("%hd", _print_int16_arg);
}

void _print_int32(int _print_int32_arg) { 
  printf("%d", _print_int32_arg);
}

void _print_int64(long long _print_int64_arg) { 
  printf("%lld", _print_int64_arg);
}

void _print_int8ptr(char* _print_int8ptr_arg) { 
  printf("%s", _print_int8ptr_arg);
}

void _print_voidptr(void* _print_voidptr_arg) { 
  printf("%p", _print_voidptr_arg);
}

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
char* str_int8ptr(char* str_int8ptr_s) { 
  return sdsnew(str_int8ptr_s);
}

char* str_printf_int8ptr(char* str_printf_int8ptr_fmt, ...) { 
  va_list str_printf_int8ptr_listx;
  c_va_start(str_printf_int8ptr_listx, str_printf_int8ptr_fmt);
  return sdscatvprintf(sdsempty(), str_printf_int8ptr_fmt, str_printf_int8ptr_listx);
}

char* empty_str() { 
  return sdsempty();
}

char* clone_int8ptr(char* clone_int8ptr_s) { 
  return sdsdup(clone_int8ptr_s);
}

void clear_int8ptr(char* clear_int8ptr_s) { 
  sdsclear(clear_int8ptr_s);
}

char* copy_int8ptr_int8ptr(char* copy_int8ptr_int8ptr_s, char* copy_int8ptr_int8ptr_t) { 
  return sdscpy(copy_int8ptr_int8ptr_s, copy_int8ptr_int8ptr_t);
}

long long len_int8ptr(char* len_int8ptr_s) { 
  return sdslen(len_int8ptr_s);
}

char* substr_int8ptr_int64_int64(char* substr_int8ptr_int64_int64_s, long long substr_int8ptr_int64_int64_start, long long substr_int8ptr_int64_int64_send) { 
  sdsrange(substr_int8ptr_int64_int64_s, substr_int8ptr_int64_int64_start, substr_int8ptr_int64_int64_send);
  return substr_int8ptr_int64_int64_s;
}

char* concat_int8ptr_int8ptr(char* concat_int8ptr_int8ptr_s, char* concat_int8ptr_int8ptr_t) { 
  return sdscatsds(concat_int8ptr_int8ptr_s, concat_int8ptr_int8ptr_t);
}

char* concat_printf_int8ptr_int8ptr(char* concat_printf_int8ptr_int8ptr_s, char* concat_printf_int8ptr_int8ptr_fmt, ...) { 
  va_list concat_printf_int8ptr_int8ptr_listx;
  c_va_start(concat_printf_int8ptr_int8ptr_listx, concat_printf_int8ptr_int8ptr_fmt);
  return sdscatvprintf(concat_printf_int8ptr_int8ptr_s, concat_printf_int8ptr_int8ptr_fmt, concat_printf_int8ptr_int8ptr_listx);
}

char* trim_int8ptr_int8ptr(char* trim_int8ptr_int8ptr_s, char* trim_int8ptr_int8ptr_cset) { 
  return sdstrim(trim_int8ptr_int8ptr_s, trim_int8ptr_int8ptr_cset);
}

int compare_int8ptr_int8ptr(char* compare_int8ptr_int8ptr_s, char* compare_int8ptr_int8ptr_s2) { 
  return sdscmp(compare_int8ptr_int8ptr_s, compare_int8ptr_int8ptr_s2);
}

char* to_lower_int8ptr(char* to_lower_int8ptr_s) { 
  sdstolower(to_lower_int8ptr_s);
  return to_lower_int8ptr_s;
}

char* to_upper_int8ptr(char* to_upper_int8ptr_s) { 
  sdstoupper(to_upper_int8ptr_s);
  return to_upper_int8ptr_s;
}

char* join_voidptr_int32_int8ptr(void* join_voidptr_int32_int8ptr_argv, int join_voidptr_int32_int8ptr_argc, char* join_voidptr_int32_int8ptr_sep) { 
  return sdsjoin(join_voidptr_int32_int8ptr_argv, join_voidptr_int32_int8ptr_argc, join_voidptr_int32_int8ptr_sep);
}

char* to_str_bool(char to_str_bool_value) { 
  if (to_str_bool_value == true) {
          return str_int8ptr("true");
    }
  else {
     return str_int8ptr("false");
    }
}

char* to_str_int64(long long to_str_int64_value) { 
  return sdsfromlonglong(to_str_int64_value);
}

char* to_str_voidptr(void* to_str_voidptr_value) { 
  return str_printf_int8ptr("%p", to_str_voidptr_value);
}

int main() { 
  char* main_mystr = concat_printf_int8ptr_int8ptr(str_int8ptr("Hello "), "%s (%d + %d = %d)", "You", 1, 2, 3);
  _print_int8ptr(concat_int8ptr_int8ptr(main_mystr, str_int8ptr("\nIt's sunny outside")));
  return 0;
}

