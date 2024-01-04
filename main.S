# strnToU64_str: -8(%rbp)
# strnToU64_len: -16(%rbp)
# strnToU64_nr: -32(%rbp)
# strnToU64_strEnd: -40(%rbp)
# fun strnToU64((*int8)(str), (int64)(len))
# 	((int64)(strnToU64_nr) = 0)
# 	((int8*)(strnToU64_strEnd) = ((int8*)(strnToU64_str) + (int64)(strnToU64_len)))
# 	while ((int8*)(strnToU64_str) < (int8*)(strnToU64_strEnd))
# 		printf("DBG: %d\n", (*(int8*)(strnToU64_str) - 48))
# 		((int64)(strnToU64_nr) = (((int64)(strnToU64_nr) * 10) + (*(int8*)(strnToU64_str) - 48)))
# 		((int8*)(strnToU64_str) = ((int8*)(strnToU64_str) + 1))
# 	ret (int64)(strnToU64_nr)
strnToU64:
push %rbp
mov %rsp, %rbp
sub $48, %rsp
movq %rsi, -16(%rbp)
movq %rdi, -8(%rbp)
# ((int64)(strnToU64_nr) = 0)
movq $0, %rax
movq %rax, -32(%rbp)
# ((int8*)(strnToU64_strEnd) = ((int8*)(strnToU64_str) + (int64)(strnToU64_len)))
leaq -8(%rbp), %rax
movq (%rax), %rax
movq -16(%rbp), %rbx
addq %rbx, %rax
leaq -40(%rbp), %rbx
movq %rax, (%rbx)
# while ((int8*)(strnToU64_str) < (int8*)(strnToU64_strEnd))
# 	printf("DBG: %d\n", (*(int8*)(strnToU64_str) - 48))
# 	((int64)(strnToU64_nr) = (((int64)(strnToU64_nr) * 10) + (*(int8*)(strnToU64_str) - 48)))
# 	((int8*)(strnToU64_str) = ((int8*)(strnToU64_str) + 1))
L0:
leaq -8(%rbp), %rax
movq (%rax), %rax
leaq -40(%rbp), %rbx
movq (%rbx), %rbx
cmp %rbx, %rax
jge L1
# printf("DBG: %d\n", (*(int8*)(strnToU64_str) - 48))
leaq -8(%rbp), %rbx
movq (%rbx), %rbx
movb (%rbx), %bl
movsx %rbx, %bl
movq $48, %r10
subb %r10, %bl
movb %bl, %sil
leaq str_0(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
# ((int64)(strnToU64_nr) = (((int64)(strnToU64_nr) * 10) + (*(int8*)(strnToU64_str) - 48)))
movq -32(%rbp), %rbx
movq $10, %rax
imulq %rbx, %rax
leaq -8(%rbp), %rbx
movq (%rbx), %rbx
movb (%rbx), %bl
movsx %rbx, %bl
movq $48, %rcx
subb %rcx, %bl
addq %bl, %rax
movq %rax, -32(%rbp)
# ((int8*)(strnToU64_str) = ((int8*)(strnToU64_str) + 1))
leaq -8(%rbp), %rbx
movq (%rbx), %rbx
movq $1, %rax
addq %rax, %rbx
leaq -8(%rbp), %rax
movq %rbx, (%rax)
jmp L0
L1:
# ret (int64)(strnToU64_nr)
movq -32(%rbp), %rbx
movq %rbx, %rax
leave
ret
# main_res: -16(%rbp)
# fun main()
# 	((int64)(main_res) = strnToU64("16", 2))
# 	printf("%d", (int64)(main_res))
# 	ret 0
main:
push %rbp
mov %rsp, %rbp
sub $16, %rsp
# ((int64)(main_res) = strnToU64("16", 2))
# strnToU64("16", 2)
movq $2, %rbx
movq %rbx, %rsi
leaq str_1(%rip), %rbx
movq %rbx, %rdi
call strnToU64
movq %rax, -16(%rbp)
# printf("%d", (int64)(main_res))
movq -16(%rbp), %rbx
movq %rbx, %rsi
leaq str_2(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
# ret 0
movq $0, %rbx
movq %rbx, %rax
leave
ret

.extern printf
.extern exit
.global strnToU64
.global main

.data
str_0: .asciz "DBG: %d\n"
str_1: .asciz "16"
str_2: .asciz "%d"
