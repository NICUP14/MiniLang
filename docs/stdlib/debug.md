# Debug library

Source: [include/stdlib/debug.ml](../../include/stdlib/debug.ml)

Provides customizable rust-like assertables and panic macros.

## Macros

Macro | Description
------------|------------
`assert_exit` | Prints the default assert message and exits
`panic_exit`  | Prints the default panic message and exits
`panic`       | Prints the given message and calls `panic_exit`
`panicf`      | Prints the formatted message and calls `panic_exit`
`assert`      | Calls `assert_exit` if the condition evaluates to `false`
`assert_eq`   | Calls `assert_exit` if the expressions are equal
`assert_neq`  | Calls `assert_exit` if the expressions are unequal

## Customizability

> [!IMPORTANT]
> To customize the message displayed by the `panic` and `assert`, override the `assert_exit` and `panic_exit` macros.

```txt
import stdlib.debug
import stdlib.io.print
import stdlib.c.cstdlib

macro panic_exit
    print("Super custom panic message!")
    exit(1)
end

fun main
    panic("Oh no!")
    ret 0
end
```
