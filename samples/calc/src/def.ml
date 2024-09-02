struct _tok_type
    err: int64
    num: int64
    add: int64
    sub: int64
    div: int64
    mult: int64
end

struct tok
    type: int64
    value: c_str
end

macro tok_type
    _tok_type(
        0, 1, 2, 3, 4, 5)
end
