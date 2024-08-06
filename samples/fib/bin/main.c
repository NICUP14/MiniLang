#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

void print_fib_int64(long long print_fib_int64_num) { 
  long long print_fib_int64_term1 = 1;
  long long print_fib_int64_term2 = 1;
  long long print_fib_int64_term3 = 0;
  while (print_fib_int64_term3 < print_fib_int64_num) {
    (print_fib_int64_term1 = print_fib_int64_term2);
    (print_fib_int64_term2 = print_fib_int64_term3);
    (print_fib_int64_term3 = (print_fib_int64_term1 + print_fib_int64_term2));
    printf("%lld ", print_fib_int64_term3);;
    }
}

long long main() { 
  print_fib_int64(100);
  return 0;
}

