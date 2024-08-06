#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

void fizz_buzz_int64(long long fizz_buzz_int64_num) { 
  long long fizz_buzz_int64_idx = 1;
  while (fizz_buzz_int64_idx <= fizz_buzz_int64_num) {
    if ((fizz_buzz_int64_idx % 15) == 0) {
        printf("%lld: FizzBuzz\n", fizz_buzz_int64_idx);
        }
    else if ((fizz_buzz_int64_idx % 3) == 0) {
     printf("%lld: Fizz\n", fizz_buzz_int64_idx);
        }
    else if ((fizz_buzz_int64_idx % 5) == 0) {
     printf("%lld: Buzz\n", fizz_buzz_int64_idx);
        }
    (fizz_buzz_int64_idx = (fizz_buzz_int64_idx + 1));;
    }
}

long long main() { 
  fizz_buzz_int64(15);
  return 0;
}

