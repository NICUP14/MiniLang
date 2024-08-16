literal("#include <re.h>")

import stdlib.c.cdef
import stdlib.io.print
# import stdlib.string

extern struct re_t
alias re = re_t

# Compiles a regex from a c string
extern fun re_compile(pattern: c_str): re
# Find matches of the txt pattern inside text (will compile automatically first)
extern fun re_matchp(pattern: re, text: c_str, matchlength: c_int*): c_int
# Find matches of the compiled pattern inside text
extern fun re_match(pattern: c_str, text: c_str, matchlength: c_int*): c_int

struct match_info
    match_idx: c_int
    match_len: c_int
    match_success: bool
end

# Enables printing of 'match_info' struct
fun _print(st: c_stream, arg: match_info): void
    print_to(st, "match_info(match_idx=", arg.match_idx, ", match_len=", arg.match_len, ", match_success=", arg.match_success, ")")
end

fun re(pattern: c_str): re
    ret re_compile(pattern)
end

fun search(pattern: re, text: c_str): bool
    let matchlength: c_int = 0
    let idx = re_matchp(pattern, text, &matchlength)
    ret idx > 0
end

fun match(pattern: re, text: c_str): match_info
    let matchlength: c_int = 0
    let idx = re_matchp(pattern, text, &matchlength)
    ret match_info(idx, matchlength, idx > 0)
end

fun match(pattern: c_str, text: c_str): match_info
    ret match(re(pattern), text)
end

# Not a performant solution!
fun replace(pattern: c_str, from: c_str, to: c_str): str
    let mlen = 0
    let idx = re_match(pattern, from, &mlen)

    let s = empty_str
    let curr = str(from)
    let sep = str(to)
    while idx >= 0
        let sub = empty_str if idx - 1 < 0 else curr.substr(0, idx - 1)
        let rest = curr.substr(idx + len(sep), 0 - 1)
        s = (s.concat(sub).
               concat(sep))
        
        curr = rest
        idx = re_match(pattern, curr, &mlen)
    end

    ret s
end

fun found(arg: match_info): bool
    ret arg.match_success
end

fun get_len(arg: match_info): int64
    if arg.match_success == false
        panic("Attempt to grab index fom unsucesfull match")
    end

    ret arg.match_idx
end

fun get_idx(arg: match_info): int64
    if arg.match_success == false
        panic("Attempt to grab index fom unsucesfull match")
    end

    ret arg.match_idx
end