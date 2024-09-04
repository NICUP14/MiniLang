# Makefile

Managing `MiniLang` project using the `GNU make` build tool.

## Project skeleton structure

```txt
skel/
├── include
│   ├── gc.c
│   ├── gc.h
│   ├── gc-LICENSE
│   ├── log.c
│   ├── log.h
│   ├── sds.c
│   ├── sds.h
│   ├── sdsalloc.h
│   └── sds-LICENSE
├── Makefile
└── src
    └── main.ml
```

## Recipes

Recipe   | Alias  | Backend
---------|--------|--------
default  | def, c | c
cdebug   | cdbg   | c
debug    | dbg    | ml
assemble | asm    | asm

## Parameters

> [!WARNING]
> For new ML projects, makefile parameters `ML`, `MLLIB` need to be adjusted if they are specified by a relative path.

Parameter | Description
----------|------------------------------
CC        | Path to c compiler
ML        | Path to ML compiler
MLLIB     | Path to ML standard library
CFLAGS    | Options passed to c compiler
MLFLAGS   | Options passed to ML compiler
