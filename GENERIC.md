# Generic plan of action

1. Change lexer to interpret "\[.*\]" as pack.
2. Then in post-process it's expanded based on the previous token.
    * var[...] => Array access
    * fun[...] => Generic specialization
    * [...] => Array literal
