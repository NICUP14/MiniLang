main:
push %rbp
mov %rsp, %rbp
sub $48, %rsp
movq $0, %rax
movq %rax, -16(%rbp)
leaq -24(%rbp), %rbx
movq $0, %rax
movq $4, %rcx
imulq %rax, %rcx
subq %rcx, %rbx
movq $5, %rax
movl %eax, (%rbx)
leaq -24(%rbp), %rbx
movq $1, %rax
movq $4, %rcx
imulq %rax, %rcx
subq %rcx, %rbx
movq $4, %rax
movl %eax, (%rbx)
leaq -24(%rbp), %rbx
movq $2, %rax
movq $4, %rcx
imulq %rax, %rcx
subq %rcx, %rbx
movq $3, %rax
movl %eax, (%rbx)
leaq -24(%rbp), %rbx
movq $3, %rax
movq $4, %rcx
imulq %rax, %rcx
subq %rcx, %rbx
movq $2, %rax
movl %eax, (%rbx)
leaq -24(%rbp), %rbx
movq $4, %rax
movq $4, %rcx
imulq %rax, %rcx
subq %rcx, %rbx
movq $1, %rax
movl %eax, (%rbx)
L0:
movq -16(%rbp), %rbx
movq $5, %rax
cmp %rax, %rbx
jge L1
leaq -24(%rbp), %rbx
movq -16(%rbp), %r10
movq $4, %r11
imulq %r10, %r11
subq %r11, %rbx
movl (%rbx), %ebx
movsx %ebx, %rbx
movq %rbx, %rsi
leaq str_0(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
movq -16(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -16(%rbp)
jmp L0
L1:
movq $0, %rbx
movq %rbx, %rax
leave
ret

.extern exit
.extern printf
.extern strlen
.global main

.data
str_0: .asciz "%d"
