#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#include <stdarg.h>
#define c_va_start va_start
#define c_va_arg va_arg
void* va_arg_va_list_voidptr(va_list va_arg_va_list_voidptr_list, void* va_arg_va_list_voidptr_argx) { 
  return c_va_arg(va_arg_va_list_voidptr_list, void*);
}

long long va_arg_va_list_int64(va_list va_arg_va_list_int64_list, long long va_arg_va_list_int64_argx) { 
  return (long long)c_va_arg(va_arg_va_list_int64_list, long long);
}

long long cond_bool_int64_int64(char cond_bool_int64_int64_maybe, long long cond_bool_int64_int64_tval, long long cond_bool_int64_int64_fval) { 
  long long cond_bool_int64_int64_val = (0 - 1);
  if (cond_bool_int64_int64_maybe == true) {
      (cond_bool_int64_int64_val = cond_bool_int64_int64_tval);
    }
  else {
   (cond_bool_int64_int64_val = cond_bool_int64_int64_fval);
    }
  return cond_bool_int64_int64_val;
}

long long _max_int64(long long _max_int64_cnt, ...) { 
  va_list _max_int64_listx;
  c_va_start(_max_int64_listx, _max_int64_cnt);
  long long _max_int64_idx = 0;
  long long _max_int64_arg = 0;
  long long _max_int64_maxx = 0;
  long long _max_int64_ccnt = _max_int64_cnt;
  while (_max_int64_idx < _max_int64_ccnt) {
    (_max_int64_arg = (long long)c_va_arg(_max_int64_listx, long long));
    (_max_int64_maxx = cond_bool_int64_int64((_max_int64_arg > _max_int64_maxx), _max_int64_arg, _max_int64_maxx));
    (_max_int64_idx = (_max_int64_idx + 1));;
    }
  return _max_int64_maxx;
}

long long main() { 
  long long main_mx = _max_int64(5, 1, 2, 3, 4, 5);
  printf("Max: %lld", main_mx);
  return 0;
}

