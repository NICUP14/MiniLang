# | asm(".macro printf_rsp fmt")
.macro printf_rsp fmt
# | asm("   lea \fmt, %rdi")
   lea \fmt, %rdi
# | asm("   mov %rsp, %rsi")
   mov %rsp, %rsi
# | asm("   xor %rax, %rax")
   xor %rax, %rax
# | asm("   call printf")
   call printf
# | asm(".endm")
.endm
# | fun main()
# |   if ((((((10 * 5) - (6 / 2)) + (8 * (4 / 2))) - (5 + 3)) == 55) == false)
# |         printf("Assertion failed, file %s, line %lld.", "main", 19)
# |     exit(1)
# |   end
# |   if (((((20 / 4) * ((15 - 3) + (6 * 2))) - (10 + 5)) == 105) == false)
# |         printf("Assertion failed, file %s, line %lld.", "main", 23)
# |     exit(1)
# |   end
# |   if (((((20 / 3) % 2) + ((30 / 4) % 3)) == 1) == false)
# |         printf("Assertion failed, file %s, line %lld.", "main", 27)
# |     exit(1)
# |   end
# |   if (((((35 / 6) * 4) + ((28 / 5) % 3)) == 22) == false)
# |         printf("Assertion failed, file %s, line %lld.", "main", 31)
# |     exit(1)
# |   end
# |   ret 0
main:
push %rbp
mov %rsp, %rbp
sub $16, %rsp
# | if ((((((10 * 5) - (6 / 2)) + (8 * (4 / 2))) - (5 + 3)) == 55) == false)
# |     printf("Assertion failed, file %s, line %lld.", "main", 19)
# |   exit(1)
movq $10, %rax
movq $5, %rbx
xor %rdx, %rdx
imulq %rbx, %rax
movq $6, %rbx
movq $2, %rcx
movq %rax, %rdx
movq %rbx, %rsi
movq %rdx, %rbx
movq %rsi, %rdx
xor %rdx, %rdx
idiv %rcx
movq $10, %rbx
subq %rax, %rbx
movq $4, %rcx
movq $2, %rdx
movq %rax, %rsi
movq %rdx, %r8
movq %rdi, %rdx
movq %r8, %rdi
movq %rcx, %rdx
movq %rsi, %rcx
movq %rdx, %rsi
xor %rdx, %rdx
idiv %rdi
movq $8, %rcx
xor %rdx, %rdx
imulq %rax, %rcx
addq %rcx, %rbx
movq $5, %rax
movq $3, %rcx
addq %rcx, %rax
subq %rax, %rbx
movq $55, %rax
cmp %rax, %rbx
sete %bl
movb $0, %al
cmp %al, %bl
jne L0
# | printf("Assertion failed, file %s, line %lld.", "main", 19)
movq $19, %rax
movq %rax, %rdx
leaq str_0(%rip), %rax
movq %rax, %rsi
leaq str_1(%rip), %rax
movq %rax, %rdi
xor %rax, %rax
call printf
# | exit(1)
movq $1, %rax
movq %rax, %rdi
call exit
L0:
# | if (((((20 / 4) * ((15 - 3) + (6 * 2))) - (10 + 5)) == 105) == false)
# |     printf("Assertion failed, file %s, line %lld.", "main", 23)
# |   exit(1)
movq $20, %rax
movq $4, %rbx
xor %rdx, %rdx
idiv %rbx
movq $15, %rbx
movq $3, %rcx
subq %rcx, %rbx
movq $6, %rcx
movq $2, %rdx
xor %rdx, %rdx
imulq %rdx, %rcx
addq %rcx, %rbx
xor %rdx, %rdx
imulq %rbx, %rax
movq $10, %rbx
movq $5, %rcx
addq %rcx, %rbx
subq %rbx, %rax
movq $105, %rbx
cmp %rbx, %rax
sete %al
movb $0, %bl
cmp %bl, %al
jne L1
# | printf("Assertion failed, file %s, line %lld.", "main", 23)
movq $23, %rax
movq %rax, %rdx
leaq str_0(%rip), %rax
movq %rax, %rsi
leaq str_1(%rip), %rax
movq %rax, %rdi
xor %rax, %rax
call printf
# | exit(1)
movq $1, %rax
movq %rax, %rdi
call exit
L1:
# | if (((((20 / 3) % 2) + ((30 / 4) % 3)) == 1) == false)
# |     printf("Assertion failed, file %s, line %lld.", "main", 27)
# |   exit(1)
movq $20, %rax
movq $3, %rbx
xor %rdx, %rdx
idiv %rbx
movq $2, %rbx
xor %rdx, %rdx
idiv %rbx
movq $30, %rax
movq $4, %rbx
xor %rdx, %rdx
idiv %rbx
movq $3, %rbx
movq %rdx, %rcx
xor %rdx, %rdx
idiv %rbx
movq $20, %rcx
addq %rdx, %rcx
movq $1, %rax
cmp %rax, %rcx
sete %cl
movb $0, %al
cmp %al, %cl
jne L2
# | printf("Assertion failed, file %s, line %lld.", "main", 27)
movq $27, %rax
movq %rax, %rdx
leaq str_0(%rip), %rax
movq %rax, %rsi
leaq str_1(%rip), %rax
movq %rax, %rdi
xor %rax, %rax
call printf
# | exit(1)
movq $1, %rax
movq %rax, %rdi
call exit
L2:
# | if (((((35 / 6) * 4) + ((28 / 5) % 3)) == 22) == false)
# |     printf("Assertion failed, file %s, line %lld.", "main", 31)
# |   exit(1)
movq $35, %rax
movq $6, %rbx
xor %rdx, %rdx
idiv %rbx
movq $4, %rbx
xor %rdx, %rdx
imulq %rbx, %rax
movq $28, %rbx
movq $5, %rcx
movq %rax, %rdx
movq %rbx, %rsi
movq %rdx, %rbx
movq %rsi, %rdx
xor %rdx, %rdx
idiv %rcx
movq $3, %rcx
xor %rdx, %rdx
idiv %rcx
movq $35, %rbx
addq %rdx, %rbx
movq $22, %rax
cmp %rax, %rbx
sete %bl
movb $0, %al
cmp %al, %bl
jne L3
# | printf("Assertion failed, file %s, line %lld.", "main", 31)
movq $31, %rax
movq %rax, %rdx
leaq str_0(%rip), %rax
movq %rax, %rsi
leaq str_1(%rip), %rax
movq %rax, %rdi
xor %rax, %rax
call printf
# | exit(1)
movq $1, %rax
movq %rax, %rdi
call exit
L3:
# | ret 0
movq $0, %rbx
movq %rbx, %rax
leave
ret
leave
ret

.extern exit
.extern printf
.global main

.data
str_0: .asciz "main"
str_1: .asciz "Assertion failed, file %s, line %lld."
