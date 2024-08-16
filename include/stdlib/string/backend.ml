literal("#include <sds.h>")

# alias sds = int8*
extern struct sds
extern struct va_list

extern fun sdslen(s: sds): int64
extern fun sdsavail(s: sds): int64 
extern fun sdssetlen(s: sds, newlen: int64): void 
extern fun sdsinclen(s: sds, inc: int64): void 
extern fun sdsalloc(s: sds): int64 
extern fun sdssetalloc(s: sds, newlen: int64): void
extern fun sdsnewlen(init: void*, initlen: int64): sds 
extern fun sdsnew(init: int8*): sds
extern fun sdsempty: sds 
extern fun sdsdup(s: sds): sds 
extern fun sdsfree(s: sds): void 
extern fun sdsgrowzero(s: sds, len: int64): sds 
extern fun sdscatlen(s: sds, t: void*, len: int64): sds 
extern fun sdscat(s: sds, t: int8*): sds 
extern fun sdscatsds(s: sds, t: sds): sds 
extern fun sdscpylen(s: sds, t: int8*, len: int64): sds 
extern fun sdscpy(s: sds, t: int8*): sds 
extern fun sdscatvprintf(s: sds, fmt: int8*, ap: va_list): sds 
extern fun sdscatprintf(s: sds, fmt: int8*, ...): sds 
extern fun sdscatfmt(s: sds, fmt: int8*, ...): sds 
extern fun sdstrim(s: sds, cset: int8*): sds 
extern fun sdsrange(s: sds, start: int64, send: int64): void 
extern fun sdsupdatelen(s: sds): void 
extern fun sdsclear(s: sds): void 
extern fun sdscmp(s1: sds, s2: sds): int32
extern fun sdssplitlen(s: int8*, len: int64, sep: int8*, seplen: int32, cnt: int32*): sds*
extern fun sdsfreesplitres(tokens: sds*, cnt: int32): void 
extern fun sdstolower(s: sds): void 
extern fun sdstoupper(s: sds): void 
extern fun sdsfromlonglong(value: int64): sds 
extern fun sdscatrepr(s: sds, p: int8*, len: int64): sds 
extern fun sdssplitargs(lline: int8*, argc: int32*): sds*
extern fun sdsmapint8s(s: sds, from: int8*, to: int8*, setlen: int64): sds 
extern fun sdsjoin(argv: int8*, argc: int32, sep: int8*): sds 
extern fun sdsjoinsds(argv: sds*, argc: int32, sep: int8*, seplen: int64): sds 
extern fun sdsMakeRoomFor(s: sds, addlen: int64): sds 
extern fun sdsIncrLen(s: sds, incr: int64): void 
extern fun sdsRemoveFreeSpace(s: sds): sds 
extern fun sdsAllocSize(s: sds): int64 
extern fun sdsAllocPtr(s: sds): void* 
extern fun sds_malloc(size: int64): void* 
extern fun sds_realloc(pointer: void*, size: int64): void* 
extern fun sds_free(pointer: void*): void 