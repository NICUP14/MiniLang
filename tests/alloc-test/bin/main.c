#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define GC_NO_GLOBAL_GC
#include <gc.h>
GarbageCollector ml_gc;
void test() { 
  long long* test_arr = (void*)0;
  (test_arr = gc_malloc(&ml_gc, 24));
  (test_arr[0] = 1);
  (test_arr[1] = 2);
  (test_arr[2] = 3);
  printf("0: %lld\n", test_arr[0]);
  printf("1: %lld\n", test_arr[1]);
  printf("2: %lld\n", test_arr[2]);
  gc_free(&ml_gc, test_arr);
  (test_arr = (void*)0);
}

int main() { 
  long long main_boss = 0;
  gc_start(&ml_gc, &main_boss);
  test();
  gc_stop(&ml_gc);
  return 0;
}

