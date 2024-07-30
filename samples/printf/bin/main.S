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
long long U64ToStrLen(long long U64ToStrLen_nr) { 
  long long U64ToStrLen_cnt = 0;
  while (U64ToStrLen_nr > 0) {
    (U64ToStrLen_nr = (U64ToStrLen_nr / 10));
    (U64ToStrLen_cnt = (U64ToStrLen_cnt + 1));;
    }
  return U64ToStrLen_cnt;
}
long long U64ToStr(long long U64ToStr_nr, char* U64ToStr_buff) { 
  long long U64ToStr_len = U64ToStrLen(U64ToStr_nr);
  long long U64ToStr_idx = (U64ToStr_len - 1);
  while (U64ToStr_nr != 0) {
    (U64ToStr_buff[U64ToStr_idx] = ((U64ToStr_nr % 10) + 48));
    (U64ToStr_idx = (U64ToStr_idx - 1));
    (U64ToStr_nr = (U64ToStr_nr / 10));;
    }
  return U64ToStr_len;
}
long long strnToU64(char* strnToU64_str, long long strnToU64_len) { 
  long long strnToU64_nr = 0;
  long long strnToU64_idx = strnToU64_len;
  while (strnToU64_idx < strnToU64_len) {
    (strnToU64_nr = ((strnToU64_nr * 10) + (strnToU64_str[strnToU64_idx] - (long long)'0')));
    (strnToU64_idx = (strnToU64_idx + 1));;
    }
  return strnToU64_nr;
}
void number(char* number_buff, long long number_num, char number_repr, char number_flag, long long number_width) { 
  char number_zf_set = ((long long)number_flag & 8);
  char number_mf_set = ((long long)number_flag & 4);
  char number_pf_set = ((long long)number_flag & 2);
  char number_sf_set = ((long long)number_flag & 1);
  char number_sign = false;
  char number_sign_ch = '_';
  char number_width_ch = '_';
  long long number_idx = 0;
  if ((long long)number_zf_set > 0) {
      (number_width_ch = '0');
}
    else {
      (number_width_ch = ' ');
    }
  if (number_num < 0) {
          (number_sign = true);
    (number_num = (0 - number_num));
    }
  if ((long long)number_repr > 0) {
          if (number_sign == true) {
        (number_sign_ch = '-');
}
      else {
              if ((long long)number_sf_set > 0) {
          (number_sign_ch = ' ');
            }
      if ((long long)number_pf_set > 0) {
          (number_sign_ch = '+');
            }
        }
    }
  puts("number before width");
  long long number_len = U64ToStrLen(number_num);
  (number_width = (number_width - U64ToStrLen(number_num)));
  if (number_width < 0) {
      (number_width = 0);
    }
  puts("number after width");
  if ((long long)number_mf_set == 0) {
          memset((void*)((long long)number_buff + number_idx), number_width_ch, number_width);
    (number_idx = (number_idx + number_width));
    }
  if ((long long)number_repr > 0) {
          if ((long long)number_sf_set > 0) {
              (number_buff[number_idx] = (long long)number_sign_ch);
      (number_idx = (number_idx + 1));
}
      else {
              if ((long long)number_pf_set > 0) {
                  (number_buff[number_idx] = (long long)number_sign_ch);
        (number_idx = (number_idx + 1));
}
        else {
                  if (number_sign == true) {
                      (number_buff[number_idx] = (long long)number_sign_ch);
          (number_idx = (number_idx + 1));
                }
            }
        }
    }
  long long number_nbytes = U64ToStr(number_num, (void*)((long long)number_buff + number_idx));
  (number_idx = (number_idx + number_nbytes));
  if ((long long)number_mf_set > 0) {
          memset((void*)((long long)number_buff + number_idx), number_width_ch, number_width);
    (number_idx = (number_idx + number_width));
    }
}
asm(".macro stack_snapshot");
asm("	push %r9");
asm("	push %r8");
asm("	push %rcx");
asm("	push %rdx");
asm("	push %rsi");
asm("	push %rdi");
asm(".endm");
asm(".macro stack_rewind");
asm("	pop %rdi");
asm("	pop %rsi");
asm("	pop %rdx");
asm("	pop %rcx");
asm("	pop %r8");
asm("	pop %r9");
asm(".endm");
long long* _va_start(long long* _va_start_list) { 
  long long _va_start_callee = ((long long)&_va_start_list + 8);
  long long* _va_start_callee_rbp = (long long*)_va_start_callee;
  long long* _va_start_caller_rbp = (long long*)*_va_start_callee_rbp;
  long long* _va_start_reg_ptr = (long long*)((long long)_va_start_callee_rbp + 24);
  long long* _va_start_stack_ptr = (long long*)((long long)_va_start_caller_rbp + 24);
  long long* _va_start_addr = malloc(48);
  memcpy(_va_start_addr, _va_start_reg_ptr, 48);
  (_va_start_list[0] = 0);
  (_va_start_list[1] = (long long)_va_start_addr);
  (_va_start_list[2] = (long long)_va_start_stack_ptr);
  return _va_start_list;
}
void _va_end(long long* _va_end_list) { 
  free((void*)((long long)_va_end_list + 8));
}
long long va_arg(long long* va_arg_list) { 
  long long va_arg_base = 0;
  long long va_arg_idx = va_arg_list[0];
  if (va_arg_list[0] <= 6) {
      (va_arg_base = va_arg_list[1]);
}
    else {
          (va_arg_base = va_arg_list[2]);
    (va_arg_idx = (va_arg_idx - 6));
    }
  (va_arg_list[0] = (va_arg_list[0] + 1));
  long long* va_arg_addr = (long long*)(va_arg_base + (va_arg_idx * 8));
  return *va_arg_addr;
}
void custom_printf(char* custom_printf_format, ...) { 
  long long custom_printf_va_list[3];
  asm("stack_snapshot");
  _va_start(custom_printf_va_list);
  va_arg(custom_printf_va_list);
  asm("stack_rewind");
  char custom_printf_flag = 0;
  char custom_printf_repeat = 0;
  char custom_printf_arr[500];
  char* custom_printf_str = custom_printf_arr;
  long long custom_printf_str_idx = 0;
  long long custom_printf_format_idx = 0;
  while (custom_printf_format[custom_printf_format_idx] != 0) {
    while (custom_printf_format[custom_printf_format_idx] != (long long)'%') {
      printf("char: '%c'\n", custom_printf_format[custom_printf_format_idx]);
      (custom_printf_str[custom_printf_str_idx] = custom_printf_format[custom_printf_format_idx]);
      if (custom_printf_format[custom_printf_format_idx] == 0) {
                  puts(custom_printf_arr);
        return ;
            }
      (custom_printf_str_idx = (custom_printf_str_idx + 1));
      (custom_printf_format_idx = (custom_printf_format_idx + 1));;
        }
    (custom_printf_flag = 0);
    (custom_printf_repeat = 1);
    while ((long long)custom_printf_repeat == 1) {
      (custom_printf_format_idx = (custom_printf_format_idx + 1));
      if (custom_printf_format[custom_printf_format_idx] == (long long)'-') {
          (custom_printf_flag = (custom_printf_flag | minus_flag));
}
        else {
                  if (custom_printf_format[custom_printf_format_idx] == (long long)'0') {
            (custom_printf_flag = (custom_printf_flag | zero_flag));
}
          else {
                      if (custom_printf_format[custom_printf_format_idx] == (long long)'+') {
              (custom_printf_flag = (custom_printf_flag | plus_flag));
}
            else {
                          if (custom_printf_format[custom_printf_format_idx] == (long long)' ') {
                (custom_printf_flag = (custom_printf_flag | space_flag));
}
              else {
                (custom_printf_repeat = 0);
                        }
                    }
                }
            };
        }
    long long custom_printf_width = 0;
    if (custom_printf_format[custom_printf_format_idx] == (long long)'*') {
        (custom_printf_width = va_arg(custom_printf_va_list));
}
      else {
              long long custom_printf_cnt = 0;
      while ((long long)isdigit(custom_printf_format[custom_printf_format_idx]) > 0) {
        (custom_printf_cnt = (custom_printf_cnt + 1));
        (custom_printf_format_idx = (custom_printf_format_idx + 1));;
            }
      if (custom_printf_cnt > 0) {
          (custom_printf_width = strnToU64((void*)((long long)(void*)((long long)custom_printf_format + custom_printf_format_idx) - custom_printf_cnt), custom_printf_cnt));
            }
        }
    if (custom_printf_format[custom_printf_format_idx] == (long long)'%') {
              (custom_printf_str[custom_printf_str_idx] = (long long)'%');
      (custom_printf_str_idx = (custom_printf_str_idx + 1));
}
      else {
              if (custom_printf_format[custom_printf_format_idx] == (long long)'s') {
                  printf("%p", custom_printf_va_list[1]);
        char* custom_printf_buf = (char*)va_arg(custom_printf_va_list);
        strcpy((void*)((long long)custom_printf_str + custom_printf_str_idx), custom_printf_buf);
        (custom_printf_str_idx = (custom_printf_str_idx + strlen(custom_printf_buf)));
}
        else {
                  if (custom_printf_format[custom_printf_format_idx] == (long long)'d') {
                      char custom_printf_repr = (char)(custom_printf_format[custom_printf_format_idx] == (long long)'d');
          long long custom_printf_num = va_arg(custom_printf_va_list);
          number((void*)((long long)custom_printf_str + custom_printf_str_idx), custom_printf_num, custom_printf_repr, custom_printf_flag, custom_printf_width);
}
          else {
                      if (custom_printf_format[custom_printf_format_idx] == (long long)'u') {
                          char custom_printf_repr = (char)(custom_printf_format[custom_printf_format_idx] == (long long)'d');
            long long custom_printf_num = va_arg(custom_printf_va_list);
            number((void*)((long long)custom_printf_str + custom_printf_str_idx), custom_printf_num, custom_printf_repr, custom_printf_flag, custom_printf_width);
                    }
                }
            }
        }
    (custom_printf_format_idx = (custom_printf_format_idx + 1));
    printf("end: %hhd\n", custom_printf_format[custom_printf_format_idx]);;
    }
  puts(custom_printf_arr);
  _va_end(custom_printf_va_list);
}
long long main() { 
  char main_repr = 1;
  char main_flag = 2;
  long long main_num = (0 - 150);
  long long main_width = 0;
  char main_buff[50];
  char* main_fmt = "Message %s %d!";
  custom_printf(main_fmt, "Hello world", 16);
  return 0;
}
