# assert_val: -8(%rbp)
# fun assert((int64)(val))
# 	if ((int64)(assert_val) == 0)
# 				printf(""Failed assertion %lld\n"", (int64)(nassert))
# 		exit(1)
# 
# 	((int64)(nassert) = ((int64)(nassert) + 1))
assert:
push %rbp
mov %rsp, %rbp
sub $16, %rsp
movq %rdi, -8(%rbp)
# if ((int64)(assert_val) == 0)
# 		printf(""Failed assertion %lld\n"", (int64)(nassert))
# 	exit(1)
# 
movq -8(%rbp), %rbx
movq $0, %rax
cmp %rax, %rbx
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
# main_my_str: -16(%rbp)
# fun main()
# ((*int64)(main_my_str) = "end\nHELLO end\nHELLO WORLD\nHELLO FROM BELOW")
main:
push %rbp
mov %rsp, %rbp
sub $16, %rsp
# ((*int64)(main_my_str) = "end\nHELLO end\nHELLO WORLD\nHELLO FROM BELOW")
leaq str_1(%rip), %rax
leaq -16(%rbp), %rbx
movq %rax, (%rbx)
leave
ret

.extern exit
.extern printf
.extern strcpy
.global assert
.global main

.data
str_0: .asciz "Failed assertion %lld\n"
str_1: .asciz "end\nHELLO end\nHELLO WORLD\nHELLO FROM BELOW"
nassert: .quad 0
