python ../../src/Main.py -C -c -I "../../include" -I src src/main.ml
long long cond(char maybe, long long tval, long long fval) { 
  long long cond_val = 0;
  if (cond_maybe == true)
      (cond_val = cond_tval)
    else
      (cond_val = cond_fval);
  };
  return cond_val;
};
long long main() { 
  long long main_c[3];
  (main_c[0] = 1);
  (main_c[1] = 2);
  (main_c[2] = 3);
  if ((long long)strcmp(type_of(true), "bool") == 0)
          if ((long long)true == 1)
        printf("Bool: true")
      else
        printf("Bool: false");
    };
  };
  if ((long long)strcmp(type_of(true), "int64") == 0)
      printf("Integer: %lld", true);
  };
  if (strchr(type_of(true), '*') != (void*)0)
      printf("Pointer: %p", true);
  };
  if (strchr(type_of(true), '&') != (void*)0)
      printf("Reference: %p", true);
  };
  if (strchr(type_of(true), '[') != (void*)0)
      printf("Arr: %p", true);
  };
  printf("\n");
  if ((long long)strcmp(type_of(false), "bool") == 0)
          if ((long long)false == 1)
        printf("Bool: true")
      else
        printf("Bool: false");
    };
  };
  if ((long long)strcmp(type_of(false), "int64") == 0)
      printf("Integer: %lld", false);
  };
  if (strchr(type_of(false), '*') != (void*)0)
      printf("Pointer: %p", false);
  };
  if (strchr(type_of(false), '&') != (void*)0)
      printf("Reference: %p", false);
  };
  if (strchr(type_of(false), '[') != (void*)0)
      printf("Arr: %p", false);
  };
  printf("\n");
  if ((long long)strcmp(type_of(&main_c), "bool") == 0)
          if ((long long)&main_c == 1)
        printf("Bool: true")
      else
        printf("Bool: false");
    };
  };
  if ((long long)strcmp(type_of(&main_c), "int64") == 0)
      printf("Integer: %lld", &main_c);
  };
  if (strchr(type_of(&main_c), '*') != (void*)0)
      printf("Pointer: %p", &main_c);
  };
  if (strchr(type_of(&main_c), '&') != (void*)0)
      printf("Reference: %p", &main_c);
  };
  if (strchr(type_of(&main_c), '[') != (void*)0)
      printf("Arr: %p", &main_c);
  };
  printf("\n");
  if ((long long)strcmp(type_of(main_c), "bool") == 0)
          if ((long long)main_c == 1)
        printf("Bool: true")
      else
        printf("Bool: false");
    };
  };
  if ((long long)strcmp(type_of(main_c), "int64") == 0)
      printf("Integer: %lld", main_c);
  };
  if (strchr(type_of(main_c), '*') != (void*)0)
      printf("Pointer: %p", main_c);
  };
  if (strchr(type_of(main_c), '&') != (void*)0)
      printf("Reference: %p", main_c);
  };
  if (strchr(type_of(main_c), '[') != (void*)0)
      printf("Arr: %p", main_c);
  };
  printf("\n");
  return 0;
}
