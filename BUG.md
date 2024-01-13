# Bugs

Solved: 6/9

- [X] Faulty load before an assignment (div).
- [X] Assignment of array rvalue to ptr type
- [X] `nr % 10 + '0'` fails due to widen.
- [X] No non-int64 ptrs/arrays due to arr_type and ptr_type.
- [ ] Save registers before calling a function.
- [X] *cstr results in a int64, not int8.
- [ ] Cannot call function as a function param.
- [X] Add declared variables to fun's offset.
- [ ] References aren't working.
