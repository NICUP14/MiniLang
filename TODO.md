# TODO

Solved: 28/40

- [ ] Add roadmap to README.
- [ ] Add generic functions to QUICKSTART.
- [ ] Document `mlpx` in `MLPX.md` and add it to README.
- [ ] Create `inject_ref` to replace `inject_copy` for `Parser._fun_call`.
- [X] Fix defers and variable assignments for control sturctures (`for`, ...).
- [X] Fix references causing errors in c backend (`&fun(...)`).
- [ ] Suggestive errors for non-existent members.
- [X] Separate macro (`delimit(" " , args)`).
- [ ] Function pointer (`&my_fun`).
- [X] Add for-loop & RAII documentation to QUICKSTART.
- [ ] Improve safety and memory safety!
- [X] Simplify compiling process (`mlpx.py`)
- [ ] Add block section to README.
- [X] Add namespace section to README.
- [X] Replace "minimal" by "easy to learn", "gentle curve" in README.
- [X] Add section at the start of README about lang-specific features.
- [ ] Add multi-lever pointers/refs (vtype: List[ckind]).
- [ ] Add const, unsigned and floating point types.
- [X] `end` no longed needed at bottom of module.

- [ ] Global arrays.
- [X] C generator backend (CWalker.py).
- [X] ML generator backend (GenStr.py -> MLWalker.py).
- [ ] ASM generator backend (Gen.py -> GenASM.py).
- [X] Fix type system.
- [X] Widen during parsing.
- [X] Static type analysis.
- [X] Check args in function call.
- [X] Include section in README regarding miscellaneous features (references, fixed-len pointers, namespaces).
- [X] Update README (#1) (new builtins, elif, ufcs, alias).
- [X] Update README (#2) (new operators, function overloading, structs).
- [X] Fix array access.
- [X] Fix array variable offset.
- [X] Implement stack alignment (align by 16-bytes).
- [X] Define operator token types (binary, unary).
- [X] Implement right-assoc.
- [X] Implement lazy loading (gen).
- [X] Add an output file parameter to the Gen module.
- [X] Improve Def.rev_type_of.
- [X] Defer.
- [X] Import.
