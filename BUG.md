# Bugs

- [ ] `nr % 10 + '0'` fails due to widen.
- [X] Faulty load before an assignment (div).
- [ ] Assignment of ptr lvalue to int literal.
- [X] Assignment of array rvalue to ptr type
- [ ] No non-int64 ptrs/arrays due to arr_type and ptr_type
- [ ] Save registers before calling a function
