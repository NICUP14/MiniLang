# main_num: -16(%rbp)
# main_x: -24(%rbp)
# fun main()
# 	((int64)(main_num) = 15)
# 	((int64)(main_x) = (&(int64)(main_num) + 15))
# 	printf("%p %lld\n", &(int64)(main_num), (int64)(main_num))
# 	ret 0
main:
push %rbp
mov %rsp, %rbp
sub $32, %rsp
# ((int64)(main_num) = 15)
movq $15, %rax
movq %rax, -16(%rbp)
# ((int64)(main_x) = (&(int64)(main_num) + 15))
leaq -16(%rbp), %rbx
movq $15, %rax
addq %rax, %rbx
movq %rbx, -24(%rbp)
# printf("%p %lld\n", &(int64)(main_num), (int64)(main_num))
movq -16(%rbp), %rbx
movq %rbx, %rdx
leaq -16(%rbp), %rbx
movq %rbx, %rsi
leaq str_0(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
# ret 0
movq $0, %rbx
movq %rbx, %rax
leave
ret

.extern exit
.extern printf
.extern scanf
.extern puts
.extern malloc
.extern free
.extern memset
.extern memcpy
.extern strlen
.extern strcpy
.extern strncpy
.extern strcmp
.extern strncmp
.extern strcat
.extern strncat
.extern strchr
.extern strrchr
.extern strstr
.extern isdigit
.extern atoi
.extern abs
.extern labs
.extern rand
.extern srand
.global main

.data
str_0: .asciz "%p %lld\n"
