# TODO

Solved: 15/20

- [ ] Global arrays.
- [ ] Generator class (unify Gen*.py `GeneratorKind` `gen(gkind) -> Generator`, `Generator.gen(out)`)
- [ ] C generator backend (GenC.py)
- [ ] ML generator backend (GenStr.py -> GenMl.py)
- [ ] ASM generator backend (Gen.py -> GenASM.py)
- [X] Fix type system.
- [X] Widen during parsing.
- [X] Static type analysis.
- [X] Check args in function call.
- [X] Include section in README regarding miscellaneous features (references, fixed-len pointers, namespaces)
- [X] Fix array access.
- [X] Fix array variable offset.
- [X] Implement stack alignment. (align by 16-bytes)
- [X] Define operator token types (binary, unary)
- [X] Implement right-assoc
- [X] Implement lazy loading (gen).
- [X] Add an output file parameter to the Gen module.
- [X] Improve Def.rev_type_of.
- [X] Defer.
- [X] Import.
