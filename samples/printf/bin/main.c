#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

char mzf_mask = 12;
char minus_flag = 8;
char zero_flag = 4;
char plus_flag = 2;
char space_flag = 1;
long long U64ToStrLen_int64(long long U64ToStrLen_int64_nr) { 
  long long U64ToStrLen_int64_cnt = 0;
  while (U64ToStrLen_int64_nr > 0) {
    (U64ToStrLen_int64_nr = (U64ToStrLen_int64_nr / 10));
    (U64ToStrLen_int64_cnt = (U64ToStrLen_int64_cnt + 1));;
    }
  return U64ToStrLen_int64_cnt;
}

long long U64ToStr_int64_int8ptr(long long U64ToStr_int64_int8ptr_nr, char* U64ToStr_int64_int8ptr_buff) { 
  long long U64ToStr_int64_int8ptr_len = U64ToStrLen_int64(U64ToStr_int64_int8ptr_nr);
  long long U64ToStr_int64_int8ptr_idx = (U64ToStr_int64_int8ptr_len - 1);
  while (U64ToStr_int64_int8ptr_nr != 0) {
    (U64ToStr_int64_int8ptr_buff[U64ToStr_int64_int8ptr_idx] = ((U64ToStr_int64_int8ptr_nr % 10) + 48));
    (U64ToStr_int64_int8ptr_idx = (U64ToStr_int64_int8ptr_idx - 1));
    (U64ToStr_int64_int8ptr_nr = (U64ToStr_int64_int8ptr_nr / 10));;
    }
  return U64ToStr_int64_int8ptr_len;
}

long long strnToU64_int8ptr_int64(char* strnToU64_int8ptr_int64_str, long long strnToU64_int8ptr_int64_len) { 
  long long strnToU64_int8ptr_int64_nr = 0;
  long long strnToU64_int8ptr_int64_idx = strnToU64_int8ptr_int64_len;
  while (strnToU64_int8ptr_int64_idx < strnToU64_int8ptr_int64_len) {
    (strnToU64_int8ptr_int64_nr = ((strnToU64_int8ptr_int64_nr * 10) + (strnToU64_int8ptr_int64_str[strnToU64_int8ptr_int64_idx] - (long long)'0')));
    (strnToU64_int8ptr_int64_idx = (strnToU64_int8ptr_int64_idx + 1));;
    }
  return strnToU64_int8ptr_int64_nr;
}

long long number_int8ptr_int64_int8_int8_int64(char* number_int8ptr_int64_int8_int8_int64_buff, long long number_int8ptr_int64_int8_int8_int64_num, char number_int8ptr_int64_int8_int8_int64_repr, char number_int8ptr_int64_int8_int8_int64_flag, long long number_int8ptr_int64_int8_int8_int64_width) { 
  char number_int8ptr_int64_int8_int8_int64_zf_set = ((long long)number_int8ptr_int64_int8_int8_int64_flag & 8);
  char number_int8ptr_int64_int8_int8_int64_mf_set = ((long long)number_int8ptr_int64_int8_int8_int64_flag & 4);
  char number_int8ptr_int64_int8_int8_int64_pf_set = ((long long)number_int8ptr_int64_int8_int8_int64_flag & 2);
  char number_int8ptr_int64_int8_int8_int64_sf_set = ((long long)number_int8ptr_int64_int8_int8_int64_flag & 1);
  char number_int8ptr_int64_int8_int8_int64_sign = false;
  char number_int8ptr_int64_int8_int8_int64_sign_ch = '_';
  char number_int8ptr_int64_int8_int8_int64_width_ch = '_';
  long long number_int8ptr_int64_int8_int8_int64_idx = 0;
  if ((long long)number_int8ptr_int64_int8_int8_int64_zf_set > 0) {
      (number_int8ptr_int64_int8_int8_int64_width_ch = '0');
    }
  else {
   (number_int8ptr_int64_int8_int8_int64_width_ch = ' ');
    }
  if (number_int8ptr_int64_int8_int8_int64_num < 0) {
          (number_int8ptr_int64_int8_int8_int64_sign = true);
    (number_int8ptr_int64_int8_int8_int64_num = (0 - number_int8ptr_int64_int8_int8_int64_num));
    }
  if ((long long)number_int8ptr_int64_int8_int8_int64_repr > 0) {
          if (number_int8ptr_int64_int8_int8_int64_sign == true) {
        (number_int8ptr_int64_int8_int8_int64_sign_ch = '-');
        }
    else {
         if ((long long)number_int8ptr_int64_int8_int8_int64_sf_set > 0) {
        (number_int8ptr_int64_int8_int8_int64_sign_ch = ' ');
        }
    else if ((long long)number_int8ptr_int64_int8_int8_int64_pf_set > 0) {
     ((long long)number_int8ptr_int64_int8_int8_int64_pf_set > 0);
        }
        }
    }
  long long number_int8ptr_int64_int8_int8_int64_len = U64ToStrLen_int64(number_int8ptr_int64_int8_int8_int64_num);
  (number_int8ptr_int64_int8_int8_int64_width = (number_int8ptr_int64_int8_int8_int64_width - U64ToStrLen_int64(number_int8ptr_int64_int8_int8_int64_num)));
  if (number_int8ptr_int64_int8_int8_int64_width < 0) {
      (number_int8ptr_int64_int8_int8_int64_width = 0);
    }
  if ((long long)number_int8ptr_int64_int8_int8_int64_mf_set == 0) {
          memset((void*)((long long)number_int8ptr_int64_int8_int8_int64_buff + number_int8ptr_int64_int8_int8_int64_idx), number_int8ptr_int64_int8_int8_int64_width_ch, number_int8ptr_int64_int8_int8_int64_width);
    (number_int8ptr_int64_int8_int8_int64_idx = (number_int8ptr_int64_int8_int8_int64_idx + number_int8ptr_int64_int8_int8_int64_width));
    }
  if ((long long)number_int8ptr_int64_int8_int8_int64_repr > 0) {
          if ((long long)number_int8ptr_int64_int8_int8_int64_sf_set > 0) {
              (number_int8ptr_int64_int8_int8_int64_buff[number_int8ptr_int64_int8_int8_int64_idx] = (long long)number_int8ptr_int64_int8_int8_int64_sign_ch);
      (number_int8ptr_int64_int8_int8_int64_idx = (number_int8ptr_int64_int8_int8_int64_idx + 1));
        }
    else {
         if ((long long)number_int8ptr_int64_int8_int8_int64_pf_set > 0) {
              (number_int8ptr_int64_int8_int8_int64_buff[number_int8ptr_int64_int8_int8_int64_idx] = (long long)number_int8ptr_int64_int8_int8_int64_sign_ch);
      (number_int8ptr_int64_int8_int8_int64_idx = (number_int8ptr_int64_int8_int8_int64_idx + 1));
        }
    else {
         if (number_int8ptr_int64_int8_int8_int64_sign == true) {
              (number_int8ptr_int64_int8_int8_int64_buff[number_int8ptr_int64_int8_int8_int64_idx] = (long long)number_int8ptr_int64_int8_int8_int64_sign_ch);
      (number_int8ptr_int64_int8_int8_int64_idx = (number_int8ptr_int64_int8_int8_int64_idx + 1));
        }
        }
        }
    }
  long long number_int8ptr_int64_int8_int8_int64_nbytes = U64ToStr_int64_int8ptr(number_int8ptr_int64_int8_int8_int64_num, (void*)((long long)number_int8ptr_int64_int8_int8_int64_buff + number_int8ptr_int64_int8_int8_int64_idx));
  (number_int8ptr_int64_int8_int8_int64_idx = (number_int8ptr_int64_int8_int8_int64_idx + number_int8ptr_int64_int8_int8_int64_nbytes));
  if ((long long)number_int8ptr_int64_int8_int8_int64_mf_set > 0) {
          memset((void*)((long long)number_int8ptr_int64_int8_int8_int64_buff + number_int8ptr_int64_int8_int8_int64_idx), number_int8ptr_int64_int8_int8_int64_width_ch, number_int8ptr_int64_int8_int8_int64_width);
    (number_int8ptr_int64_int8_int8_int64_idx = (number_int8ptr_int64_int8_int8_int64_idx + number_int8ptr_int64_int8_int8_int64_width));
    }
  return number_int8ptr_int64_int8_int8_int64_idx;
}

#include <stdarg.h>
#define c_va_start va_start
#define c_va_arg va_arg
void* va_arg_va_list_voidptr(va_list va_arg_va_list_voidptr_list, void* va_arg_va_list_voidptr_argx) { 
  return c_va_arg(va_arg_va_list_voidptr_list, void*);
}

long long va_arg_va_list_int64(va_list va_arg_va_list_int64_list, long long va_arg_va_list_int64_argx) { 
  return (long long)c_va_arg(va_arg_va_list_int64_list, int);
}

void custom_printf_int8ptr(char* custom_printf_int8ptr_format, ...) { 
  va_list custom_printf_int8ptr_va_list;
  c_va_start(custom_printf_int8ptr_va_list, custom_printf_int8ptr_format);
  char custom_printf_int8ptr_flag = 0;
  char custom_printf_int8ptr_repeat = 0;
  char custom_printf_int8ptr_arr[500];
  char* custom_printf_int8ptr_str = custom_printf_int8ptr_arr;
  long long custom_printf_int8ptr_str_idx = 0;
  long long custom_printf_int8ptr_format_idx = 0;
  while (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] != 0) {
    while (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] != (long long)'%') {
      (custom_printf_int8ptr_str[custom_printf_int8ptr_str_idx] = custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx]);
      if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == 0) {
                  puts(custom_printf_int8ptr_arr);
        return ;
            }
      (custom_printf_int8ptr_str_idx = (custom_printf_int8ptr_str_idx + 1));
      (custom_printf_int8ptr_format_idx = (custom_printf_int8ptr_format_idx + 1));;
        }
    (custom_printf_int8ptr_flag = 0);
    (custom_printf_int8ptr_repeat = 1);
    while ((long long)custom_printf_int8ptr_repeat == 1) {
      (custom_printf_int8ptr_format_idx = (custom_printf_int8ptr_format_idx + 1));
      if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'-') {
          (custom_printf_int8ptr_flag = (custom_printf_int8ptr_flag | minus_flag));
            }
      else {
             if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'0') {
          (custom_printf_int8ptr_flag = (custom_printf_int8ptr_flag | zero_flag));
            }
      else {
             if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'+') {
          (custom_printf_int8ptr_flag = (custom_printf_int8ptr_flag | plus_flag));
            }
      else {
             if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)' ') {
          (custom_printf_int8ptr_flag = (custom_printf_int8ptr_flag | space_flag));
            }
      else {
       (custom_printf_int8ptr_repeat = 0);
            }
            }
            }
            };
        }
    long long custom_printf_int8ptr_width = 0;
    if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'*') {
        (custom_printf_int8ptr_width = (long long)c_va_arg(custom_printf_int8ptr_va_list, int));
        }
    else {
         long long custom_printf_int8ptr_cnt = 0;
    while ((long long)isdigit(custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx]) > 0) {
      (custom_printf_int8ptr_cnt = (custom_printf_int8ptr_cnt + 1));
      (custom_printf_int8ptr_format_idx = (custom_printf_int8ptr_format_idx + 1));;
        }
    if (custom_printf_int8ptr_cnt > 0) {
        (custom_printf_int8ptr_width = strnToU64_int8ptr_int64((void*)((long long)(void*)((long long)custom_printf_int8ptr_format + custom_printf_int8ptr_format_idx) - custom_printf_int8ptr_cnt), custom_printf_int8ptr_cnt));
        }
        }
    if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'%') {
              (custom_printf_int8ptr_str[custom_printf_int8ptr_str_idx] = (long long)'%');
      (custom_printf_int8ptr_str_idx = (custom_printf_int8ptr_str_idx + 1));
        }
    else {
         if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'s') {
              char* custom_printf_int8ptr_buf = (char*)c_va_arg(custom_printf_int8ptr_va_list, void*);
      strcpy((void*)((long long)custom_printf_int8ptr_str + custom_printf_int8ptr_str_idx), custom_printf_int8ptr_buf);
      (custom_printf_int8ptr_str_idx = (custom_printf_int8ptr_str_idx + strlen(custom_printf_int8ptr_buf)));
        }
    else {
         if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'d') {
              char custom_printf_int8ptr_repr = (char)(custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'d');
      long long custom_printf_int8ptr_num = (long long)c_va_arg(custom_printf_int8ptr_va_list, int);
      long long custom_printf_int8ptr_off = number_int8ptr_int64_int8_int8_int64((void*)((long long)custom_printf_int8ptr_str + custom_printf_int8ptr_str_idx), custom_printf_int8ptr_num, custom_printf_int8ptr_repr, custom_printf_int8ptr_flag, custom_printf_int8ptr_width);
      (custom_printf_int8ptr_str_idx = (custom_printf_int8ptr_str_idx + custom_printf_int8ptr_off));
        }
    else {
         if (custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'u') {
              char custom_printf_int8ptr_repr = (char)(custom_printf_int8ptr_format[custom_printf_int8ptr_format_idx] == (long long)'d');
      long long custom_printf_int8ptr_num = (long long)c_va_arg(custom_printf_int8ptr_va_list, int);
      long long custom_printf_int8ptr_off = number_int8ptr_int64_int8_int8_int64((void*)((long long)custom_printf_int8ptr_str + custom_printf_int8ptr_str_idx), custom_printf_int8ptr_num, custom_printf_int8ptr_repr, custom_printf_int8ptr_flag, custom_printf_int8ptr_width);
      (custom_printf_int8ptr_str_idx = (custom_printf_int8ptr_str_idx + custom_printf_int8ptr_off));
        }
        }
        }
        }
    (custom_printf_int8ptr_format_idx = (custom_printf_int8ptr_format_idx + 1));;
    }
  puts(custom_printf_int8ptr_arr);
}

long long main() { 
  char* main_fmt = "Message %s 20%d!";
  custom_printf_int8ptr(main_fmt, "Hello world", 16);
  return 0;
}

