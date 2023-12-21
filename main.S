main:
push %rbp
mov %rsp, %rbp
sub $64, %rsp
leaq -16(%rbp), %rbx
movq $0, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq $0, %rax
movq %rax, (%rbx)
leaq -16(%rbp), %rbx
movq $1, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq $1, %rax
movq %rax, (%rbx)
leaq -16(%rbp), %rbx
movq $2, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq $2, %rax
movq %rax, (%rbx)
leaq -16(%rbp), %rbx
movq $3, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq $3, %rax
movq %rax, (%rbx)
leaq -16(%rbp), %rbx
movq $4, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq $4, %rax
movq %rax, (%rbx)
leaq -16(%rbp), %rax
leaq -64(%rbp), %rbx
movq %rax, (%rbx)
leaq -64(%rbp), %r10
movq (%r10), %r10
movq $3, %rbx
movq $8, %r11
imulq %rbx, %r11
addq %r11, %r10
movq (%r10), %r10
movq %r10, %rsi
leaq str_0(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
movq $0, %rbx
movq %rbx, %rax
leave
ret

.extern exit
.extern printf
.global main

.data
str_0: .asciz "%lld\n"
