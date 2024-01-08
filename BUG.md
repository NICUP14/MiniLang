# Bugs

Solved: 3/10

- [X] Faulty load before an assignment (div).
- [X] Assignment of array rvalue to ptr type
- [ ] `nr % 10 + '0'` fails due to widen.
- [ ] Assignment of ptr lvalue to int literal.
- [ ] No non-int64 ptrs/arrays due to arr_type and ptr_type.
- [ ] Save registers before calling a function.
- [X] *cstr results in a int64, not int8.
- [ ] Cannot call function as a function param.
- [ ] Add declared variables to fun's offset.
- [ ] References aren't working.
