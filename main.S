# assert_val: -8(%rbp)
# fun assert((int8)(val))
# 	if (widen((int8)(assert_val)) == 0)
# 				printf(""Failed assertion %lld\n"", (int64)(nassert))
# 		exit(1)
# 
# 	((int64)(nassert) = ((int64)(nassert) + 1))
assert:
push %rbp
mov %rsp, %rbp
sub $16, %rsp
movb %dil, -8(%rbp)
# if (widen((int8)(assert_val)) == 0)
# 		printf(""Failed assertion %lld\n"", (int64)(nassert))
# 	exit(1)
# 
movb -8(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jne L0
# printf(""Failed assertion %lld\n"", (int64)(nassert))
movq nassert(%rip), %rbx
movq %rbx, %rsi
leaq str_0(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
# exit(1)
movq $1, %rbx
movq %rbx, %rdi
call exit
L0:
# ((int64)(nassert) = ((int64)(nassert) + 1))
movq nassert(%rip), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, nassert(%rip)
leave
ret
# main_idx: -16(%rbp)
# main_str: -24(%rbp)
# fun main()
# 	((int64)(main_idx) = 0)
# 	((*int64)(main_str) = ""abcd"")
# 	while ((int64)(main_idx) < strlen((*int64)(main_str)))
# 		printf(""%lld %c\n"", (int64)(main_idx), (*int64)(main_str)[(int64)(main_idx)])
# 		((int64)(main_idx) = ((int64)(main_idx) + 1))
# 	ret 0
main:
push %rbp
mov %rsp, %rbp
sub $32, %rsp
# ((int64)(main_idx) = 0)
movq $0, %rax
movq %rax, -16(%rbp)
# ((*int64)(main_str) = ""abcd"")
leaq str_1(%rip), %rax
leaq -24(%rbp), %rbx
movq %rax, (%rbx)
# while ((int64)(main_idx) < strlen((*int64)(main_str)))
# 	printf(""%lld %c\n"", (int64)(main_idx), (*int64)(main_str)[(int64)(main_idx)])
# 	((int64)(main_idx) = ((int64)(main_idx) + 1))
L1:
# strlen((*int64)(main_str))
leaq -24(%rbp), %rbx
movq (%rbx), %rbx
movq %rbx, %rdi
call strlen
movq -16(%rbp), %rbx
cmp %rax, %rbx
jge L2
# printf(""%lld %c\n"", (int64)(main_idx), (*int64)(main_str)[(int64)(main_idx)])
leaq -24(%rbp), %rbx
movq (%rbx), %rbx
movq -16(%rbp), %r10
movq $8, %r11
imulq %r10, %r11
addq %r11, %rbx
movq (%rbx), %rbx
movq %rbx, %rdx
movq -16(%rbp), %rbx
movq %rbx, %rsi
leaq str_2(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
# ((int64)(main_idx) = ((int64)(main_idx) + 1))
movq -16(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -16(%rbp)
jmp L1
L2:
# ret 0
movq $0, %rbx
movq %rbx, %rax
leave
ret

.extern exit
.extern printf
.extern strlen
.global assert
.global main

.data
str_0: .asciz "Failed assertion %lld\n"
str_1: .asciz "abcd"
str_2: .asciz "%lld %c\n"
nassert: .quad 1
