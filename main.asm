.data
fmt: .asciz "%d\n"
assert_num: .quad 0
errmsg: .asciz "Assert %d failed\n"
.text
assert:
enter $0, $0
cmp $1, %dil
je LL1
lea errmsg(%rip), %rdi
mov assert_num(%rip), %rsi
xor %rax, %rax
call printf
mov $1, %rax
call exit
LL1:
addq $1, assert_num(%rip)
leave
ret
print:
enter $0, $0
mov %rdi, %rsi
lea fmt(%rip), %rdi
xor %rax, %rax
call printf
leave
ret
# fun U64ToStrLen((int64)(nr))
# 	((int64)(U64ToStrLen_cnt) = 0)
# 	while ((int64)(U64ToStrLen_nr) != 0)
# 		((int64)(U64ToStrLen_nr) = ((int64)(U64ToStrLen_nr) / 10))
# 		((int64)(U64ToStrLen_cnt) = ((int64)(U64ToStrLen_cnt) + 1))
# 	ret (int64)(U64ToStrLen_cnt)
U64ToStrLen:
push %rbp
mov %rsp, %rbp
sub $32, %rsp
movq %rdi, -8(%rbp)
# ((int64)(U64ToStrLen_cnt) = 0)
movq $0, %rax
movq %rax, -24(%rbp)
# while ((int64)(U64ToStrLen_nr) != 0)
# 	((int64)(U64ToStrLen_nr) = ((int64)(U64ToStrLen_nr) / 10))
# 	((int64)(U64ToStrLen_cnt) = ((int64)(U64ToStrLen_cnt) + 1))
L0:
movq -8(%rbp), %rbx
movq $0, %rax
cmp %rax, %rbx
je L1
# ((int64)(U64ToStrLen_nr) = ((int64)(U64ToStrLen_nr) / 10))
movq -8(%rbp), %rbx
movq $10, %rax
movq %rbx, %rcx
movq %rax, %rbx
movq %rcx, %rax
xor %rdx, %rdx
idiv %rbx
movq %rax, -8(%rbp)
# ((int64)(U64ToStrLen_cnt) = ((int64)(U64ToStrLen_cnt) + 1))
movq -24(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -24(%rbp)
jmp L0
L1:
# ret (int64)(U64ToStrLen_cnt)
movq -24(%rbp), %rbx
movq %rbx, %rax
leave
ret
# fun U64ToStr((int64)(nr), (*int64)(buff))
# 	((int64)(U64ToStr_len) = U64ToStrLen((int64)(U64ToStr_nr)))
# 	((*int64)(U64ToStr_addr) = (((*int64)(U64ToStr_buff) + (int64)(U64ToStr_len)) - 1))
# 	while ((int64)(U64ToStr_nr) != 0)
# 		(*(*int64)(U64ToStr_addr) = (((int64)(U64ToStr_nr) % 10) + 48))
# 		((int64)(U64ToStr_nr) = ((int64)(U64ToStr_nr) / 10))
# 		((*int64)(U64ToStr_addr) = ((*int64)(U64ToStr_addr) - 1))
# 	ret (int64)(U64ToStr_len)
U64ToStr:
push %rbp
mov %rsp, %rbp
sub $48, %rsp
movq %rsi, -16(%rbp)
movq %rdi, -8(%rbp)
# ((int64)(U64ToStr_len) = U64ToStrLen((int64)(U64ToStr_nr)))
# U64ToStrLen((int64)(U64ToStr_nr))
movq -8(%rbp), %rbx
movq %rbx, %rdi
call U64ToStrLen
movq %rax, -32(%rbp)
# ((*int64)(U64ToStr_addr) = (((*int64)(U64ToStr_buff) + (int64)(U64ToStr_len)) - 1))
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -32(%rbp), %rbx
addq %rbx, %rax
movq $1, %rbx
subq %rbx, %rax
leaq -40(%rbp), %rbx
movq %rax, (%rbx)
# while ((int64)(U64ToStr_nr) != 0)
# 	(*(*int64)(U64ToStr_addr) = (((int64)(U64ToStr_nr) % 10) + 48))
# 	((int64)(U64ToStr_nr) = ((int64)(U64ToStr_nr) / 10))
# 	((*int64)(U64ToStr_addr) = ((*int64)(U64ToStr_addr) - 1))
L2:
movq -8(%rbp), %rbx
movq $0, %rax
cmp %rax, %rbx
je L3
# (*(*int64)(U64ToStr_addr) = (((int64)(U64ToStr_nr) % 10) + 48))
movq -8(%rbp), %rbx
movq $10, %rax
movq %rbx, %rcx
movq %rax, %rbx
movq %rcx, %rax
xor %rdx, %rdx
idiv %rbx
movq $48, %rbx
addq %rbx, %rdx
leaq -40(%rbp), %rbx
movq (%rbx), %rbx
movb %dl, (%rbx)
# ((int64)(U64ToStr_nr) = ((int64)(U64ToStr_nr) / 10))
movq -8(%rbp), %rbx
movq $10, %rax
movq %rbx, %rcx
movq %rax, %rbx
movq %rcx, %rax
xor %rdx, %rdx
idiv %rbx
movq %rax, -8(%rbp)
# ((*int64)(U64ToStr_addr) = ((*int64)(U64ToStr_addr) - 1))
leaq -40(%rbp), %rbx
movq (%rbx), %rbx
movq $1, %rax
subq %rax, %rbx
leaq -40(%rbp), %rax
movq %rbx, (%rax)
jmp L2
L3:
# ret (int64)(U64ToStr_len)
movq -32(%rbp), %rbx
movq %rbx, %rax
leave
ret
# fun main()
# 	((*int64)(main_buff)[0] = 0)
# 	((*int64)(main_buff)[1] = 0)
# 	((*int64)(main_buff)[2] = 0)
# 	((*int64)(main_buff)[3] = 0)
# 	((*int64)(main_buff)[4] = 0)
# 	((*int64)(main_buffPtr) = (*int64)(main_buff))
# 	((int64)(main_res) = U64ToStr(6969, (*int64)(main_buff)))
# 	printf("%lld %s", (int64)(main_res), (*int64)(main_buffPtr))
# 	exit(0)
main:
push %rbp
mov %rsp, %rbp
sub $80, %rsp
# ((*int64)(main_buff)[0] = 0)
leaq -16(%rbp), %rbx
imulq %rax, %rcx
addq %rcx, %rbx
movq $0, %rax
leaq -16(%rbp), %rbx
movq %rax, (%rbx)
# ((*int64)(main_buff)[1] = 0)
leaq -16(%rbp), %rbx
imulq %rax, %rcx
addq %rcx, %rbx
movq $0, %rax
leaq -16(%rbp), %rbx
movq %rax, (%rbx)
# ((*int64)(main_buff)[2] = 0)
leaq -16(%rbp), %rbx
imulq %rax, %rcx
addq %rcx, %rbx
movq $0, %rax
leaq -16(%rbp), %rbx
movq %rax, (%rbx)
# ((*int64)(main_buff)[3] = 0)
leaq -16(%rbp), %rbx
imulq %rax, %rcx
addq %rcx, %rbx
movq $0, %rax
leaq -16(%rbp), %rbx
movq %rax, (%rbx)
# ((*int64)(main_buff)[4] = 0)
leaq -16(%rbp), %rbx
imulq %rax, %rcx
addq %rcx, %rbx
movq $0, %rax
leaq -16(%rbp), %rbx
movq %rax, (%rbx)
# ((*int64)(main_buffPtr) = (*int64)(main_buff))
leaq -16(%rbp), %rax
leaq -64(%rbp), %rbx
movq %rax, (%rbx)
# ((int64)(main_res) = U64ToStr(6969, (*int64)(main_buff)))
# U64ToStr(6969, (*int64)(main_buff))
leaq -16(%rbp), %rbx
movq %rbx, %rsi
movq $6969, %rbx
movq %rbx, %rdi
call U64ToStr
movq %rax, -72(%rbp)
# printf("%lld %s", (int64)(main_res), (*int64)(main_buffPtr))
leaq -64(%rbp), %rbx
movq (%rbx), %rbx
movq %rbx, %rdx
movq -72(%rbp), %rbx
movq %rbx, %rsi
leaq str_0(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
# exit(0)
movq $0, %rbx
movq %rbx, %rdi
call exit
leave
ret

.extern printf
.extern exit
.global U64ToStrLen
.global U64ToStr
.global main

.data
str_0: .asciz "%lld %s"
