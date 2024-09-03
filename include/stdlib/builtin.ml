# bultin.ml - The builtin module for ml.
# This module is automatically imported into the specified source by the compiler.

extern fun ptr_sub(cs: void*, cs2: void*): void*
extern fun ptr_dist(cs: void*, cs2: void*): int64

import stdlib.builtin.*
import stdlib.alloc.backend

macro default(_ident)
    cast(type_of(_ident), 0)
end