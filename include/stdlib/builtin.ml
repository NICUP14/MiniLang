# bultin.ml - The builtin module for ml.
# This module is automatically imported into the specified source by the compiler.

import stdlib.builtin.*
import stdlib.alloc.backend

macro default(_ident)
    cast(type_of(_ident), 0)
end