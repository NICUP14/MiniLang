main:
push %rbp
mov %rsp, %rbp
sub $16, %rsp
movb $0, %al
movb %al, -9(%rbp)
movb -9(%rbp), %bl
movb $0, %al
cmp %al, %bl
jne L0
leaq str_0(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
jmp L1
L0:
leaq str_1(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
L1:
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
str_0: .asciz "True"
str_1: .asciz "False"
