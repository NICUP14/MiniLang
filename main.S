assert:
push %rbp
mov %rsp, %rbp
sub $16, %rsp
movq %rdi, -8(%rbp)
movq -8(%rbp), %rbx
movq $0, %rax
cmp %rax, %rbx
jne L0
movq nassert(%rip), %rbx
movq %rbx, %rsi
leaq str_0(%rip), %rbx
movq %rbx, %rdi
xor %rax, %rax
call printf
movq $1, %rbx
movq %rbx, %rdi
call exit
L0:
movq nassert(%rip), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, nassert(%rip)
leave
ret
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
movq $4, %rax
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
movq $0, %rbx
movq $8, %r11
imulq %rbx, %r11
addq %r11, %r10
movq (%r10), %r10
movq $0, %rbx
cmp %rbx, %r10
sete %r10b
movb %r10b, %dil
call assert
leaq -64(%rbp), %r10
movq (%r10), %r10
movq $1, %rbx
movq $8, %r11
imulq %rbx, %r11
addq %r11, %r10
movq (%r10), %r10
movq $1, %rbx
cmp %rbx, %r10
sete %r10b
movb %r10b, %dil
call assert
leaq -64(%rbp), %r10
movq (%r10), %r10
movq $2, %rbx
movq $8, %r11
imulq %rbx, %r11
addq %r11, %r10
movq (%r10), %r10
movq $2, %rbx
cmp %rbx, %r10
sete %r10b
movb %r10b, %dil
call assert
leaq -64(%rbp), %r10
movq (%r10), %r10
movq $3, %rbx
movq $8, %r11
imulq %rbx, %r11
addq %r11, %r10
movq (%r10), %r10
movq $3, %rbx
cmp %rbx, %r10
sete %r10b
movb %r10b, %dil
call assert
leaq -64(%rbp), %r10
movq (%r10), %r10
movq $4, %rbx
movq $8, %r11
imulq %rbx, %r11
addq %r11, %r10
movq (%r10), %r10
movq $4, %rbx
cmp %rbx, %r10
sete %r10b
movb %r10b, %dil
call assert
movq $0, %rbx
movq %rbx, %rdi
call exit
leave
ret

.extern printf
.extern exit
.global assert
.global main

.data
str_0: .asciz "Failed assertion %lld\n"
nassert: .quad 1
