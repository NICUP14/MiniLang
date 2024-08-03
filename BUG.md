# Bugs

Solved: 12/17

- [ ] Macro-related bug (check `expand_macro`).
- [ ] Function declarations do not work inside macros (fails signature check).
- [ ] `ma_cnt` builtin is no longer working.
- [ ] Div/Mod bug (Doesn't check `in_reg` == `rax`)
- [X] Implicit cast arr-ptr/ref doesn't work (Def.type_compatible).
- [ ] Cast in macro allows this: `cast("int64", (1, 2, 3))`.
- [X] Passing arguments from variadic macro to fun doesn't work.
- [ ] Assignment/At-related bug (also in macros) (`"15" = 5`/`"15" at (12 + 1)`).
- [X] Cannot call function as a function param.
- [X] No type checking for reference and dereference (`*bool = int64`).
- [X] Faulty load before an assignment (div).
- [X] Assignment of array rvalue to ptr type
- [X] `nr % 10 + '0'` fails due to widen.
- [X] No non-int64 ptrs/arrays due to arr_type and ptr_type.
- [X] Save registers before calling a function.
- [X] *cstr results in a int64, not int8.
- [X] Add declared variables to fun's offset.
- [X] References aren't working.
