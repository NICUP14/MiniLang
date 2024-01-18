# Bugs

Solved: 8/12

- [X] Passing arguments from variadic macro to fun doesn't work.
- [ ] Assignment/At-related bug (also in macros) (`"15" = 5`/`"15" at (12 + 1)`).
- [ ] Cannot call function as a function param.
- [X] No type checking for reference and dereference (`*bool = int64`).
- [X] Faulty load before an assignment (div).
- [X] Assignment of array rvalue to ptr type
- [X] `nr % 10 + '0'` fails due to widen.
- [X] No non-int64 ptrs/arrays due to arr_type and ptr_type.
- [X] Save registers before calling a function.
- [X] *cstr results in a int64, not int8.
- [X] Add declared variables to fun's offset.
- [X] References aren't working.
