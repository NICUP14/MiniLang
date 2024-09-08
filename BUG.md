# Bugs

Solved: 23/28

- [X] No type checking when passing sig to fun.
- [X] Bug with functions returning refs.
- [ ] Create Def.fun_locals.
- [ ] Macros cause buggy behaviour with UFCS.
- [ ] Make that control structures create blocks.
- [X] `Parser.ref` does not implicit cast-to-ref (add `try_cast_ref`)
- [X] Functions like `input` are predeferred.
- [X] Using an iterator `i` in a for loop does not compile correctly.
- [X] Nested UFCS expressions (s.equals("Hello".str))
- [X] The type of an overloaded function with a diff type than the first takes the type of the first overloaded function
- [X] Pointer to struct displayed as "long long*". (no name field in elem_ckind)
- [X] Struct elements pollute the global scope with non-existent variables.
- [X] Cannot call function as struct method with only one arg.
- [ ] Function declarations do not work inside macros (fails signature check).
- [X] Macro-related bug (check `expand_macro`).
- [X] `ma_cnt` builtin is no longer working.
- [ ] Div/Mod bug for asm backend (Doesn't check `in_reg` == `rax`)
- [X] Implicit cast arr-ptr/ref doesn't work (Def.type_compatible).
- [X] Passing arguments from variadic macro to fun doesn't work.
- [X] Assignment/At-related bug (also in macros) (`"15" = 5`/`"15" at (12 + 1)`).
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
