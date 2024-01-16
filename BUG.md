# Bugs

Solved: 7/10

- [ ] tests/test/main.ml:cast_malloc not working.
- [ ] Cannot call function as a function param.
- [ ] No type checking for reference and dereference (`*bool = int64`).
- [X] Faulty load before an assignment (div).
- [X] Assignment of array rvalue to ptr type
- [X] `nr % 10 + '0'` fails due to widen.
- [X] No non-int64 ptrs/arrays due to arr_type and ptr_type.
- [X] Save registers before calling a function.
- [X] *cstr results in a int64, not int8.
- [X] Add declared variables to fun's offset.
- [X] References aren't working.
