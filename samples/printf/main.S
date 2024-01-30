# | U64ToStrLen_nr: -16(%rbp)
# | U64ToStrLen_cnt: -24(%rbp)
# | fun U64ToStrLen((int64)(nr))
# |   ((int64)(U64ToStrLen_cnt) = 0)
# |   while ((int64)(U64ToStrLen_nr) > 0)
# |     ((int64)(U64ToStrLen_nr) = ((int64)(U64ToStrLen_nr) / 10))
# |     ((int64)(U64ToStrLen_cnt) = ((int64)(U64ToStrLen_cnt) + 1))
# |   end
# |   ret (int64)(U64ToStrLen_cnt)
U64ToStrLen:
push %rbp
mov %rsp, %rbp
sub $32, %rsp
movq %rdi, -16(%rbp)
# | ((int64)(U64ToStrLen_cnt) = 0)
movq $0, %rax
movq %rax, -24(%rbp)
# | while ((int64)(U64ToStrLen_nr) > 0)
# |   ((int64)(U64ToStrLen_nr) = ((int64)(U64ToStrLen_nr) / 10))
# |   ((int64)(U64ToStrLen_cnt) = ((int64)(U64ToStrLen_cnt) + 1))
L0:
movq -16(%rbp), %rbx
movq $0, %rax
cmp %rax, %rbx
jle L1
# | ((int64)(U64ToStrLen_nr) = ((int64)(U64ToStrLen_nr) / 10))
movq -16(%rbp), %rbx
movq $10, %rax
movq %rbx, %rcx
movq %rax, %rbx
movq %rcx, %rax
xor %rdx, %rdx
idiv %rbx
movq %rax, -16(%rbp)
# | ((int64)(U64ToStrLen_cnt) = ((int64)(U64ToStrLen_cnt) + 1))
movq -24(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -24(%rbp)
jmp L0
L1:
# | ret (int64)(U64ToStrLen_cnt)
movq -24(%rbp), %rbx
movq %rbx, %rax
leave
ret
# | U64ToStrLen_nr: -16(%rbp)
# | U64ToStrLen_cnt: -24(%rbp)
# | U64ToStr_nr: -16(%rbp)
# | U64ToStr_buff: -24(%rbp)
# | U64ToStr_len: -32(%rbp)
# | U64ToStr_idx: -40(%rbp)
# | fun U64ToStr((int64)(nr), (int8*)(buff))
# |   ((int64)(U64ToStr_len) = U64ToStrLen((int64)(U64ToStr_nr)))
# |   ((int64)(U64ToStr_idx) = ((int64)(U64ToStr_len) - 1))
# |   while ((int64)(U64ToStr_nr) != 0)
# |     ((int8*)(U64ToStr_buff)[(int64)(U64ToStr_idx)] = (((int64)(U64ToStr_nr) % 10) + 48))
# |     ((int64)(U64ToStr_idx) = ((int64)(U64ToStr_idx) - 1))
# |     ((int64)(U64ToStr_nr) = ((int64)(U64ToStr_nr) / 10))
# |   end
# |   ret (int64)(U64ToStr_len)
U64ToStr:
push %rbp
mov %rsp, %rbp
sub $48, %rsp
movq %rsi, -24(%rbp)
movq %rdi, -16(%rbp)
# | ((int64)(U64ToStr_len) = U64ToStrLen((int64)(U64ToStr_nr)))
# | U64ToStrLen((int64)(U64ToStr_nr))
movq -16(%rbp), %rax
movq %rax, %rdi
call U64ToStrLen
movq %rax, -32(%rbp)
# | ((int64)(U64ToStr_idx) = ((int64)(U64ToStr_len) - 1))
movq -32(%rbp), %rbx
movq $1, %rax
subq %rax, %rbx
movq %rbx, -40(%rbp)
# | while ((int64)(U64ToStr_nr) != 0)
# |   ((int8*)(U64ToStr_buff)[(int64)(U64ToStr_idx)] = (((int64)(U64ToStr_nr) % 10) + 48))
# |   ((int64)(U64ToStr_idx) = ((int64)(U64ToStr_idx) - 1))
# |   ((int64)(U64ToStr_nr) = ((int64)(U64ToStr_nr) / 10))
L2:
movq -16(%rbp), %rbx
movq $0, %rax
cmp %rax, %rbx
je L3
# | ((int8*)(U64ToStr_buff)[(int64)(U64ToStr_idx)] = (((int64)(U64ToStr_nr) % 10) + 48))
leaq -24(%rbp), %rax
movq (%rax), %rax
movq -40(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movq -16(%rbp), %rcx
movq $10, %rbx
movq %rax, %rdx
movq %rax, %rsi
xor %rdx, %rdx
idiv %rcx
movq $48, %rcx
addq %rcx, %rdx
movb %dl, (%rdx)
# | ((int64)(U64ToStr_idx) = ((int64)(U64ToStr_idx) - 1))
movq -40(%rbp), %rbx
movq $1, %rax
subq %rax, %rbx
movq %rbx, -40(%rbp)
# | ((int64)(U64ToStr_nr) = ((int64)(U64ToStr_nr) / 10))
movq -16(%rbp), %rbx
movq $10, %rax
movq %rbx, %rcx
movq %rax, %rbx
movq %rcx, %rax
xor %rdx, %rdx
idiv %rbx
movq %rax, -16(%rbp)
jmp L2
L3:
# | ret (int64)(U64ToStr_len)
movq -32(%rbp), %rbx
movq %rbx, %rax
leave
ret
# | strnToU64_str: -16(%rbp)
# | strnToU64_len: -24(%rbp)
# | strnToU64_nr: -32(%rbp)
# | strnToU64_idx: -40(%rbp)
# | fun strnToU64((int8*)(str), (int64)(len))
# |   ((int64)(strnToU64_nr) = 0)
# |   ((int64)(strnToU64_idx) = (int64)(strnToU64_len))
# |   while ((int64)(strnToU64_idx) < (int64)(strnToU64_len))
# |     ((int64)(strnToU64_nr) = (((int64)(strnToU64_nr) * 10) + ((int8*)(strnToU64_str)[(int64)(strnToU64_idx)] - widen('0'))))
# |     ((int64)(strnToU64_idx) = ((int64)(strnToU64_idx) + 1))
# |   end
# |   ret (int64)(strnToU64_nr)
strnToU64:
push %rbp
mov %rsp, %rbp
sub $48, %rsp
movq %rsi, -24(%rbp)
movq %rdi, -16(%rbp)
# | ((int64)(strnToU64_nr) = 0)
movq $0, %rax
movq %rax, -32(%rbp)
# | ((int64)(strnToU64_idx) = (int64)(strnToU64_len))
movq -24(%rbp), %rax
movq %rax, -40(%rbp)
# | while ((int64)(strnToU64_idx) < (int64)(strnToU64_len))
# |   ((int64)(strnToU64_nr) = (((int64)(strnToU64_nr) * 10) + ((int8*)(strnToU64_str)[(int64)(strnToU64_idx)] - widen('0'))))
# |   ((int64)(strnToU64_idx) = ((int64)(strnToU64_idx) + 1))
L4:
movq -40(%rbp), %rax
movq -24(%rbp), %rbx
cmp %rbx, %rax
jge L5
# | ((int64)(strnToU64_nr) = (((int64)(strnToU64_nr) * 10) + ((int8*)(strnToU64_str)[(int64)(strnToU64_idx)] - widen('0'))))
movq -32(%rbp), %rbx
movq $10, %rax
xor %rdx, %rdx
imulq %rax, %rbx
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -40(%rbp), %rcx
movq $1, %rdx
imulq %rcx, %rdx
addq %rdx, %rax
movb (%rax), %al
movsx %al, %rax
movb $48, %cl
movsx %cl, %rcx
subq %rcx, %rax
addq %rax, %rbx
movq %rbx, -32(%rbp)
# | ((int64)(strnToU64_idx) = ((int64)(strnToU64_idx) + 1))
movq -40(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -40(%rbp)
jmp L4
L5:
# | ret (int64)(strnToU64_nr)
movq -32(%rbp), %rbx
movq %rbx, %rax
leave
ret
# | number_buff: -16(%rbp)
# | number_num: -24(%rbp)
# | number_repr: -25(%rbp)
# | number_flag: -26(%rbp)
# | number_width: -34(%rbp)
# | number_zf_set: -35(%rbp)
# | number_mf_set: -36(%rbp)
# | number_pf_set: -37(%rbp)
# | number_sf_set: -38(%rbp)
# | number_sign: -39(%rbp)
# | number_sign_ch: -40(%rbp)
# | number_width_ch: -41(%rbp)
# | number_idx: -49(%rbp)
# | number_len: -57(%rbp)
# | number_nbytes: -65(%rbp)
# | fun number((int8*)(buff), (int64)(num), (int8)(repr), (int8)(flag), (int64)(width))
# |   ((int8)(number_zf_set) = (widen((int8)(number_flag)) & 8))
# |   ((int8)(number_mf_set) = (widen((int8)(number_flag)) & 4))
# |   ((int8)(number_pf_set) = (widen((int8)(number_flag)) & 2))
# |   ((int8)(number_sf_set) = (widen((int8)(number_flag)) & 1))
# |   ((bool)(number_sign) = false)
# |   ((int8)(number_sign_ch) = '_')
# |   ((int8)(number_width_ch) = '_')
# |   ((int64)(number_idx) = 0)
# |   if (widen((int8)(number_zf_set)) > 0)
# |     ((int8)(number_width_ch) = '0')
# |   else
# |     ((int8)(number_width_ch) = ' ')
# |   end
# |   if ((int64)(number_num) < 0)
# |         ((bool)(number_sign) = true)
# |     ((int64)(number_num) = (0 - (int64)(number_num)))
# |   end
# |   if (widen((int8)(number_repr)) > 0)
# |         if ((bool)(number_sign) == true)
# |       ((int8)(number_sign_ch) = '-')
# |     else
# |             if (widen((int8)(number_sf_set)) > 0)
# |         ((int8)(number_sign_ch) = ' ')
# |       end
# |       if (widen((int8)(number_pf_set)) > 0)
# |         ((int8)(number_sign_ch) = '+')
# |       end
# |     end
# |   end
# |   puts("number before width")
# |   ((int64)(number_len) = U64ToStrLen((int64)(number_num)))
# |   ((int64)(number_width) = ((int64)(number_width) - U64ToStrLen((int64)(number_num))))
# |   if ((int64)(number_width) < 0)
# |     ((int64)(number_width) = 0)
# |   end
# |   puts("number after width")
# |   if (widen((int8)(number_mf_set)) == 0)
# |         memset(cast("void*", (cast("int64", (int8*)(number_buff)) + (int64)(number_idx))), (int8)(number_width_ch), (int64)(number_width))
# |     ((int64)(number_idx) = ((int64)(number_idx) + (int64)(number_width)))
# |   end
# |   if (widen((int8)(number_repr)) > 0)
# |         if (widen((int8)(number_sf_set)) > 0)
# |             ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |       ((int64)(number_idx) = ((int64)(number_idx) + 1))
# |     else
# |             if (widen((int8)(number_pf_set)) > 0)
# |                 ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |         ((int64)(number_idx) = ((int64)(number_idx) + 1))
# |       else
# |                 if ((bool)(number_sign) == true)
# |                     ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |           ((int64)(number_idx) = ((int64)(number_idx) + 1))
# |         end
# |       end
# |     end
# |   end
# |   ((int64)(number_nbytes) = U64ToStr((int64)(number_num), cast("void*", (cast("int64", (int8*)(number_buff)) + (int64)(number_idx)))))
# |   ((int64)(number_idx) = ((int64)(number_idx) + (int64)(number_nbytes)))
# |   if (widen((int8)(number_mf_set)) > 0)
# |         memset(cast("void*", (cast("int64", (int8*)(number_buff)) + (int64)(number_idx))), (int8)(number_width_ch), (int64)(number_width))
# |     ((int64)(number_idx) = ((int64)(number_idx) + (int64)(number_width)))
# |   end
number:
push %rbp
mov %rsp, %rbp
sub $80, %rsp
movq %r8, -34(%rbp)
movb %cl, -26(%rbp)
movb %dl, -25(%rbp)
movq %rsi, -24(%rbp)
movq %rdi, -16(%rbp)
# | ((int8)(number_zf_set) = (widen((int8)(number_flag)) & 8))
movb -26(%rbp), %al
movsx %al, %rax
movq $8, %rbx
andq %rbx, %rax
movb %al, -35(%rbp)
# | ((int8)(number_mf_set) = (widen((int8)(number_flag)) & 4))
movb -26(%rbp), %al
movsx %al, %rax
movq $4, %rbx
andq %rbx, %rax
movb %al, -36(%rbp)
# | ((int8)(number_pf_set) = (widen((int8)(number_flag)) & 2))
movb -26(%rbp), %al
movsx %al, %rax
movq $2, %rbx
andq %rbx, %rax
movb %al, -37(%rbp)
# | ((int8)(number_sf_set) = (widen((int8)(number_flag)) & 1))
movb -26(%rbp), %al
movsx %al, %rax
movq $1, %rbx
andq %rbx, %rax
movb %al, -38(%rbp)
# | ((bool)(number_sign) = false)
movb $0, %al
movb %al, -39(%rbp)
# | ((int8)(number_sign_ch) = '_')
movb $95, %al
movb %al, -40(%rbp)
# | ((int8)(number_width_ch) = '_')
movb $95, %al
movb %al, -41(%rbp)
# | ((int64)(number_idx) = 0)
movq $0, %rax
movq %rax, -49(%rbp)
# | if (widen((int8)(number_zf_set)) > 0)
# |   ((int8)(number_width_ch) = '0')
# | else
# |   ((int8)(number_width_ch) = ' ')
movb -35(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jle L6
# | ((int8)(number_width_ch) = '0')
movb $48, %al
movb %al, -41(%rbp)
jmp L7
L6:
# | ((int8)(number_width_ch) = ' ')
movb $32, %al
movb %al, -41(%rbp)
L7:
# | if ((int64)(number_num) < 0)
# |     ((bool)(number_sign) = true)
# |   ((int64)(number_num) = (0 - (int64)(number_num)))
movq -24(%rbp), %rbx
movq $0, %rax
cmp %rax, %rbx
jge L8
# | ((bool)(number_sign) = true)
movb $1, %al
movb %al, -39(%rbp)
# | ((int64)(number_num) = (0 - (int64)(number_num)))
movq $0, %rax
movq -24(%rbp), %rbx
subq %rbx, %rax
movq %rax, -24(%rbp)
L8:
# | if (widen((int8)(number_repr)) > 0)
# |     if ((bool)(number_sign) == true)
# |     ((int8)(number_sign_ch) = '-')
# |   else
# |         if (widen((int8)(number_sf_set)) > 0)
# |       ((int8)(number_sign_ch) = ' ')
# |     end
# |     if (widen((int8)(number_pf_set)) > 0)
# |       ((int8)(number_sign_ch) = '+')
# |     end
# |   end
movb -25(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jle L9
# | if ((bool)(number_sign) == true)
# |   ((int8)(number_sign_ch) = '-')
# | else
# |     if (widen((int8)(number_sf_set)) > 0)
# |     ((int8)(number_sign_ch) = ' ')
# |   end
# |   if (widen((int8)(number_pf_set)) > 0)
# |     ((int8)(number_sign_ch) = '+')
# |   end
movb -39(%rbp), %bl
movb $1, %al
cmp %al, %bl
jne L10
# | ((int8)(number_sign_ch) = '-')
movb $45, %al
movb %al, -40(%rbp)
jmp L11
L10:
# | if (widen((int8)(number_sf_set)) > 0)
# |   ((int8)(number_sign_ch) = ' ')
movb -38(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jle L12
# | ((int8)(number_sign_ch) = ' ')
movb $32, %al
movb %al, -40(%rbp)
L12:
# | if (widen((int8)(number_pf_set)) > 0)
# |   ((int8)(number_sign_ch) = '+')
movb -37(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jle L13
# | ((int8)(number_sign_ch) = '+')
movb $43, %al
movb %al, -40(%rbp)
L13:
L11:
L9:
# | puts("number before width")
leaq str_0(%rip), %rax
movq %rax, %rdi
call puts
# | ((int64)(number_len) = U64ToStrLen((int64)(number_num)))
# | U64ToStrLen((int64)(number_num))
movq -24(%rbp), %rax
movq %rax, %rdi
call U64ToStrLen
movq %rax, -57(%rbp)
# | ((int64)(number_width) = ((int64)(number_width) - U64ToStrLen((int64)(number_num))))
# | U64ToStrLen((int64)(number_num))
movq -24(%rbp), %rax
movq %rax, %rdi
call U64ToStrLen
movq -34(%rbp), %rbx
subq %rax, %rbx
movq %rbx, -34(%rbp)
# | if ((int64)(number_width) < 0)
# |   ((int64)(number_width) = 0)
movq -34(%rbp), %rbx
movq $0, %rax
cmp %rax, %rbx
jge L14
# | ((int64)(number_width) = 0)
movq $0, %rax
movq %rax, -34(%rbp)
L14:
# | puts("number after width")
leaq str_1(%rip), %rax
movq %rax, %rdi
call puts
# | if (widen((int8)(number_mf_set)) == 0)
# |     memset(cast("void*", (cast("int64", (int8*)(number_buff)) + (int64)(number_idx))), (int8)(number_width_ch), (int64)(number_width))
# |   ((int64)(number_idx) = ((int64)(number_idx) + (int64)(number_width)))
movb -36(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jne L15
# | memset(cast("void*", (cast("int64", (int8*)(number_buff)) + (int64)(number_idx))), (int8)(number_width_ch), (int64)(number_width))
movq -34(%rbp), %rax
movq %rax, %rdx
movb -41(%rbp), %al
movb %al, %sil
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -49(%rbp), %rbx
addq %rbx, %rax
movq %rax, %rdi
call memset
# | ((int64)(number_idx) = ((int64)(number_idx) + (int64)(number_width)))
movq -49(%rbp), %rax
movq -34(%rbp), %rbx
addq %rbx, %rax
movq %rax, -49(%rbp)
L15:
# | if (widen((int8)(number_repr)) > 0)
# |     if (widen((int8)(number_sf_set)) > 0)
# |         ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |     ((int64)(number_idx) = ((int64)(number_idx) + 1))
# |   else
# |         if (widen((int8)(number_pf_set)) > 0)
# |             ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |       ((int64)(number_idx) = ((int64)(number_idx) + 1))
# |     else
# |             if ((bool)(number_sign) == true)
# |                 ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |         ((int64)(number_idx) = ((int64)(number_idx) + 1))
# |       end
# |     end
# |   end
movb -25(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jle L16
# | if (widen((int8)(number_sf_set)) > 0)
# |     ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |   ((int64)(number_idx) = ((int64)(number_idx) + 1))
# | else
# |     if (widen((int8)(number_pf_set)) > 0)
# |         ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |     ((int64)(number_idx) = ((int64)(number_idx) + 1))
# |   else
# |         if ((bool)(number_sign) == true)
# |             ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |       ((int64)(number_idx) = ((int64)(number_idx) + 1))
# |     end
# |   end
movb -38(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jle L17
# | ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -49(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb -40(%rbp), %bl
movsx %bl, %rbx
movb %bl, (%rax)
# | ((int64)(number_idx) = ((int64)(number_idx) + 1))
movq -49(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -49(%rbp)
jmp L18
L17:
# | if (widen((int8)(number_pf_set)) > 0)
# |     ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |   ((int64)(number_idx) = ((int64)(number_idx) + 1))
# | else
# |     if ((bool)(number_sign) == true)
# |         ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |     ((int64)(number_idx) = ((int64)(number_idx) + 1))
# |   end
movb -37(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jle L19
# | ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -49(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb -40(%rbp), %bl
movsx %bl, %rbx
movb %bl, (%rax)
# | ((int64)(number_idx) = ((int64)(number_idx) + 1))
movq -49(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -49(%rbp)
jmp L20
L19:
# | if ((bool)(number_sign) == true)
# |     ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
# |   ((int64)(number_idx) = ((int64)(number_idx) + 1))
movb -39(%rbp), %bl
movb $1, %al
cmp %al, %bl
jne L21
# | ((int8*)(number_buff)[(int64)(number_idx)] = widen((int8)(number_sign_ch)))
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -49(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb -40(%rbp), %bl
movsx %bl, %rbx
movb %bl, (%rax)
# | ((int64)(number_idx) = ((int64)(number_idx) + 1))
movq -49(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -49(%rbp)
L21:
L20:
L18:
L16:
# | ((int64)(number_nbytes) = U64ToStr((int64)(number_num), cast("void*", (cast("int64", (int8*)(number_buff)) + (int64)(number_idx)))))
# | U64ToStr((int64)(number_num), cast("void*", (cast("int64", (int8*)(number_buff)) + (int64)(number_idx))))
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -49(%rbp), %rbx
addq %rbx, %rax
movq %rax, %rsi
movq -24(%rbp), %rax
movq %rax, %rdi
call U64ToStr
movq %rax, -65(%rbp)
# | ((int64)(number_idx) = ((int64)(number_idx) + (int64)(number_nbytes)))
movq -49(%rbp), %rax
movq -65(%rbp), %rbx
addq %rbx, %rax
movq %rax, -49(%rbp)
# | if (widen((int8)(number_mf_set)) > 0)
# |     memset(cast("void*", (cast("int64", (int8*)(number_buff)) + (int64)(number_idx))), (int8)(number_width_ch), (int64)(number_width))
# |   ((int64)(number_idx) = ((int64)(number_idx) + (int64)(number_width)))
movb -36(%rbp), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
jle L22
# | memset(cast("void*", (cast("int64", (int8*)(number_buff)) + (int64)(number_idx))), (int8)(number_width_ch), (int64)(number_width))
movq -34(%rbp), %rax
movq %rax, %rdx
movb -41(%rbp), %al
movb %al, %sil
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -49(%rbp), %rbx
addq %rbx, %rax
movq %rax, %rdi
call memset
# | ((int64)(number_idx) = ((int64)(number_idx) + (int64)(number_width)))
movq -49(%rbp), %rax
movq -34(%rbp), %rbx
addq %rbx, %rax
movq %rax, -49(%rbp)
L22:
leave
ret
# | asm(".macro stack_snapshot")
.macro stack_snapshot
# | asm("	push %r9")
	push %r9
# | asm("	push %r8")
	push %r8
# | asm("	push %rcx")
	push %rcx
# | asm("	push %rdx")
	push %rdx
# | asm("	push %rsi")
	push %rsi
# | asm("	push %rdi")
	push %rdi
# | asm(".endm")
.endm
# | asm(".macro stack_rewind")
.macro stack_rewind
# | asm("	pop %rdi")
	pop %rdi
# | asm("	pop %rsi")
	pop %rsi
# | asm("	pop %rdx")
	pop %rdx
# | asm("	pop %rcx")
	pop %rcx
# | asm("	pop %r8")
	pop %r8
# | asm("	pop %r9")
	pop %r9
# | asm(".endm")
.endm
# | _va_start_list: -16(%rbp)
# | _va_start_callee: -24(%rbp)
# | _va_start_callee_rbp: -32(%rbp)
# | _va_start_caller_rbp: -40(%rbp)
# | _va_start_reg_ptr: -48(%rbp)
# | _va_start_stack_ptr: -56(%rbp)
# | _va_start_addr: -64(%rbp)
# | fun _va_start((int64*)(list))
# |   ((int64)(_va_start_callee) = (cast("int64", &(int64*)(_va_start_list)) + 8))
# |   ((int64*)(_va_start_callee_rbp) = cast("int64*", (int64)(_va_start_callee)))
# |   ((int64*)(_va_start_caller_rbp) = cast("int64*", *(int64*)(_va_start_callee_rbp)))
# |   ((int64*)(_va_start_reg_ptr) = cast("int64*", (cast("int64", (int64*)(_va_start_callee_rbp)) + 24)))
# |   ((int64*)(_va_start_stack_ptr) = cast("int64*", (cast("int64", (int64*)(_va_start_caller_rbp)) + 24)))
# |   ((int64*)(_va_start_addr) = malloc(48))
# |   memcpy((int64*)(_va_start_addr), (int64*)(_va_start_reg_ptr), 48)
# |   ((int64*)(_va_start_list)[0] = 0)
# |   ((int64*)(_va_start_list)[1] = cast("int64", (int64*)(_va_start_addr)))
# |   ((int64*)(_va_start_list)[2] = cast("int64", (int64*)(_va_start_stack_ptr)))
# |   ret (int64*)(_va_start_list)
_va_start:
push %rbp
mov %rsp, %rbp
sub $64, %rsp
movq %rdi, -16(%rbp)
# | ((int64)(_va_start_callee) = (cast("int64", &(int64*)(_va_start_list)) + 8))
leaq -16(%rbp), %rbx
movq $8, %rax
addq %rax, %rbx
movq %rbx, -24(%rbp)
# | ((int64*)(_va_start_callee_rbp) = cast("int64*", (int64)(_va_start_callee)))
movq -24(%rbp), %rax
leaq -32(%rbp), %rbx
movq %rax, (%rbx)
# | ((int64*)(_va_start_caller_rbp) = cast("int64*", *(int64*)(_va_start_callee_rbp)))
leaq -32(%rbp), %rax
movq (%rax), %rax
movq (%rax), %rax
leaq -40(%rbp), %rbx
movq %rax, (%rbx)
# | ((int64*)(_va_start_reg_ptr) = cast("int64*", (cast("int64", (int64*)(_va_start_callee_rbp)) + 24)))
leaq -32(%rbp), %rbx
movq (%rbx), %rbx
movq $24, %rax
addq %rax, %rbx
leaq -48(%rbp), %rax
movq %rbx, (%rax)
# | ((int64*)(_va_start_stack_ptr) = cast("int64*", (cast("int64", (int64*)(_va_start_caller_rbp)) + 24)))
leaq -40(%rbp), %rbx
movq (%rbx), %rbx
movq $24, %rax
addq %rax, %rbx
leaq -56(%rbp), %rax
movq %rbx, (%rax)
# | ((int64*)(_va_start_addr) = malloc(48))
# | malloc(48)
movq $48, %rax
movq %rax, %rdi
call malloc
leaq -64(%rbp), %rbx
movq %rax, (%rbx)
# | memcpy((int64*)(_va_start_addr), (int64*)(_va_start_reg_ptr), 48)
movq $48, %rax
movq %rax, %rdx
leaq -48(%rbp), %rax
movq (%rax), %rax
movq %rax, %rsi
leaq -64(%rbp), %rax
movq (%rax), %rax
movq %rax, %rdi
call memcpy
# | ((int64*)(_va_start_list)[0] = 0)
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq $0, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq $0, %rax
movq %rax, (%rbx)
# | ((int64*)(_va_start_list)[1] = cast("int64", (int64*)(_va_start_addr)))
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq $1, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
leaq -64(%rbp), %rax
movq (%rax), %rax
movq %rax, (%rbx)
# | ((int64*)(_va_start_list)[2] = cast("int64", (int64*)(_va_start_stack_ptr)))
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq $2, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
leaq -56(%rbp), %rax
movq (%rax), %rax
movq %rax, (%rbx)
# | ret (int64*)(_va_start_list)
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq %rbx, %rax
leave
ret
# | _va_end_list: -16(%rbp)
# | fun _va_end((int64*)(list))
# |   free((int64*)(_va_end_list)[1])
_va_end:
push %rbp
mov %rsp, %rbp
sub $16, %rsp
movq %rdi, -16(%rbp)
# | free((int64*)(_va_end_list)[1])
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq $1, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq (%rbx), %rbx
movq %rbx, %rdi
call free
leave
ret
# | va_arg_list: -16(%rbp)
# | va_arg_base: -24(%rbp)
# | va_arg_idx: -32(%rbp)
# | va_arg_addr: -40(%rbp)
# | fun va_arg((int64*)(list))
# |   ((int64)(va_arg_base) = 0)
# |   ((int64)(va_arg_idx) = (int64*)(va_arg_list)[0])
# |   if ((int64*)(va_arg_list)[0] <= 6)
# |     ((int64)(va_arg_base) = (int64*)(va_arg_list)[1])
# |   else
# |         ((int64)(va_arg_base) = (int64*)(va_arg_list)[2])
# |     ((int64)(va_arg_idx) = ((int64)(va_arg_idx) - 6))
# |   end
# |   ((int64*)(va_arg_list)[0] = ((int64*)(va_arg_list)[0] + 1))
# |   ((int64*)(va_arg_addr) = cast("int64*", ((int64)(va_arg_base) + ((int64)(va_arg_idx) * 8))))
# |   ret *(int64*)(va_arg_addr)
va_arg:
push %rbp
mov %rsp, %rbp
sub $48, %rsp
movq %rdi, -16(%rbp)
# | ((int64)(va_arg_base) = 0)
movq $0, %rax
movq %rax, -24(%rbp)
# | ((int64)(va_arg_idx) = (int64*)(va_arg_list)[0])
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq $0, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq (%rbx), %rbx
movq %rbx, -32(%rbp)
# | if ((int64*)(va_arg_list)[0] <= 6)
# |   ((int64)(va_arg_base) = (int64*)(va_arg_list)[1])
# | else
# |     ((int64)(va_arg_base) = (int64*)(va_arg_list)[2])
# |   ((int64)(va_arg_idx) = ((int64)(va_arg_idx) - 6))
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq $0, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq (%rbx), %rbx
movq $6, %rax
cmp %rax, %rbx
jg L23
# | ((int64)(va_arg_base) = (int64*)(va_arg_list)[1])
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq $1, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq (%rbx), %rbx
movq %rbx, -24(%rbp)
jmp L24
L23:
# | ((int64)(va_arg_base) = (int64*)(va_arg_list)[2])
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq $2, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
movq (%rbx), %rbx
movq %rbx, -24(%rbp)
# | ((int64)(va_arg_idx) = ((int64)(va_arg_idx) - 6))
movq -32(%rbp), %rbx
movq $6, %rax
subq %rax, %rbx
movq %rbx, -32(%rbp)
L24:
# | ((int64*)(va_arg_list)[0] = ((int64*)(va_arg_list)[0] + 1))
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq $0, %rax
movq $8, %rcx
imulq %rax, %rcx
addq %rcx, %rbx
leaq -16(%rbp), %rcx
movq (%rcx), %rcx
movq $0, %rax
movq $8, %rdx
imulq %rax, %rdx
addq %rdx, %rcx
movq (%rcx), %rcx
movq $1, %rax
addq %rax, %rcx
movq %rcx, (%rbx)
# | ((int64*)(va_arg_addr) = cast("int64*", ((int64)(va_arg_base) + ((int64)(va_arg_idx) * 8))))
movq -32(%rbp), %rbx
movq $8, %rax
xor %rdx, %rdx
imulq %rax, %rbx
movq -24(%rbp), %rax
addq %rbx, %rax
leaq -40(%rbp), %rbx
movq %rax, (%rbx)
# | ret *(int64*)(va_arg_addr)
leaq -40(%rbp), %rbx
movq (%rbx), %rbx
movq (%rbx), %rbx
movq %rbx, %rax
leave
ret
# | custom_printf_format: -16(%rbp)
# | custom_printf_va_list: -40(%rbp)
# | custom_printf_flag: -41(%rbp)
# | custom_printf_repeat: -42(%rbp)
# | custom_printf_arr: -542(%rbp)
# | custom_printf_str: -550(%rbp)
# | custom_printf_str_idx: -558(%rbp)
# | custom_printf_format_idx: -566(%rbp)
# | custom_printf_width: -574(%rbp)
# | custom_printf_cnt: -582(%rbp)
# | custom_printf_buf: -590(%rbp)
# | custom_printf_repr: -600(%rbp)
# | custom_printf_num: -608(%rbp)
# | fun custom_printf((int8*)(format), ...)
# |   asm("stack_snapshot")
# |   _va_start((int64[3])(custom_printf_va_list))
# |   va_arg((int64[3])(custom_printf_va_list))
# |   asm("stack_rewind")
# |   ((int8)(custom_printf_flag) = 0)
# |   ((int8)(custom_printf_repeat) = 0)
# |   ((int8*)(custom_printf_str) = (int8[500])(custom_printf_arr))
# |   ((int64)(custom_printf_str_idx) = 0)
# |   ((int64)(custom_printf_format_idx) = 0)
# |   while ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] != 0)
# |     while ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] != widen('%'))
# |       ((int8*)(custom_printf_str)[(int64)(custom_printf_str_idx)] = (int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)])
# |       ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |       ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + 1))
# |     end
# |     ((int8)(custom_printf_flag) = 0)
# |     ((int8)(custom_printf_repeat) = 1)
# |     while (widen((int8)(custom_printf_repeat)) == 1)
# |       ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |       if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('-'))
# |         ((int8)(custom_printf_flag) = (int8)(minus_flag))
# |       else
# |                 if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('0'))
# |           ((int8)(custom_printf_flag) = (int8)(zero_flag))
# |         else
# |                     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('+'))
# |             ((int8)(custom_printf_flag) = (int8)(plus_flag))
# |           else
# |                         if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen(' '))
# |               ((int8)(custom_printf_flag) = (int8)(space_flag))
# |             else
# |               ((int8)(custom_printf_repeat) = 0)
# |             end
# |           end
# |         end
# |       end
# |     end
# |     ((int64)(custom_printf_width) = 0)
# |     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('*'))
# |       ((int64)(custom_printf_width) = va_arg((int64[3])(custom_printf_va_list)))
# |     else
# |             ((int64)(custom_printf_cnt) = 0)
# |       while (widen(isdigit((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)])) > 0)
# |         ((int64)(custom_printf_cnt) = ((int64)(custom_printf_cnt) + 1))
# |         ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |       end
# |       if ((int64)(custom_printf_cnt) > 0)
# |         ((int64)(custom_printf_width) = strnToU64(cast("void*", (cast("int64", cast("void*", (cast("int64", (int8*)(custom_printf_format)) + (int64)(custom_printf_format_idx)))) - (int64)(custom_printf_cnt))), (int64)(custom_printf_cnt)))
# |       end
# |     end
# |     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('%'))
# |             ((int8*)(custom_printf_str)[(int64)(custom_printf_str_idx)] = widen('%'))
# |       ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + 1))
# |     else
# |             if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('s'))
# |                 ((int8*)(custom_printf_buf) = cast("int8*", va_arg((int64[3])(custom_printf_va_list))))
# |         strcpy(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int8*)(custom_printf_buf))
# |         ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + strlen((int8*)(custom_printf_buf))))
# |       else
# |                 if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))
# |                     ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |           ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |           number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# |         else
# |                     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('u'))
# |                         ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |             ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |             number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# |           end
# |         end
# |       end
# |     end
# |     ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |   end
# |   puts((int8[500])(custom_printf_arr))
# |   _va_end((int64[3])(custom_printf_va_list))
custom_printf:
push %rbp
mov %rsp, %rbp
sub $608, %rsp
movq %rdi, -16(%rbp)
# | asm("stack_snapshot")
stack_snapshot
# | _va_start((int64[3])(custom_printf_va_list))
leaq -40(%rbp), %rax
movq %rax, %rdi
call _va_start
# | va_arg((int64[3])(custom_printf_va_list))
leaq -40(%rbp), %rax
movq %rax, %rdi
call va_arg
# | asm("stack_rewind")
stack_rewind
# | ((int8)(custom_printf_flag) = 0)
movq $0, %rax
movb %al, -41(%rbp)
# | ((int8)(custom_printf_repeat) = 0)
movq $0, %rax
movb %al, -42(%rbp)
# | ((int8*)(custom_printf_str) = (int8[500])(custom_printf_arr))
leaq -542(%rbp), %rax
leaq -550(%rbp), %rbx
movq %rax, (%rbx)
# | ((int64)(custom_printf_str_idx) = 0)
movq $0, %rax
movq %rax, -558(%rbp)
# | ((int64)(custom_printf_format_idx) = 0)
movq $0, %rax
movq %rax, -566(%rbp)
# | while ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] != 0)
# |   while ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] != widen('%'))
# |     ((int8*)(custom_printf_str)[(int64)(custom_printf_str_idx)] = (int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)])
# |     ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |     ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + 1))
# |   end
# |   ((int8)(custom_printf_flag) = 0)
# |   ((int8)(custom_printf_repeat) = 1)
# |   while (widen((int8)(custom_printf_repeat)) == 1)
# |     ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('-'))
# |       ((int8)(custom_printf_flag) = (int8)(minus_flag))
# |     else
# |             if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('0'))
# |         ((int8)(custom_printf_flag) = (int8)(zero_flag))
# |       else
# |                 if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('+'))
# |           ((int8)(custom_printf_flag) = (int8)(plus_flag))
# |         else
# |                     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen(' '))
# |             ((int8)(custom_printf_flag) = (int8)(space_flag))
# |           else
# |             ((int8)(custom_printf_repeat) = 0)
# |           end
# |         end
# |       end
# |     end
# |   end
# |   ((int64)(custom_printf_width) = 0)
# |   if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('*'))
# |     ((int64)(custom_printf_width) = va_arg((int64[3])(custom_printf_va_list)))
# |   else
# |         ((int64)(custom_printf_cnt) = 0)
# |     while (widen(isdigit((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)])) > 0)
# |       ((int64)(custom_printf_cnt) = ((int64)(custom_printf_cnt) + 1))
# |       ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |     end
# |     if ((int64)(custom_printf_cnt) > 0)
# |       ((int64)(custom_printf_width) = strnToU64(cast("void*", (cast("int64", cast("void*", (cast("int64", (int8*)(custom_printf_format)) + (int64)(custom_printf_format_idx)))) - (int64)(custom_printf_cnt))), (int64)(custom_printf_cnt)))
# |     end
# |   end
# |   if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('%'))
# |         ((int8*)(custom_printf_str)[(int64)(custom_printf_str_idx)] = widen('%'))
# |     ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + 1))
# |   else
# |         if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('s'))
# |             ((int8*)(custom_printf_buf) = cast("int8*", va_arg((int64[3])(custom_printf_va_list))))
# |       strcpy(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int8*)(custom_printf_buf))
# |       ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + strlen((int8*)(custom_printf_buf))))
# |     else
# |             if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))
# |                 ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |         ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |         number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# |       else
# |                 if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('u'))
# |                     ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |           ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |           number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# |         end
# |       end
# |     end
# |   end
# |   ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
L25:
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movq $0, %rbx
cmp %rbx, %rax
je L26
# | while ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] != widen('%'))
# |   ((int8*)(custom_printf_str)[(int64)(custom_printf_str_idx)] = (int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)])
# |   ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |   ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + 1))
L27:
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $37, %bl
movsx %bl, %rbx
cmp %rbx, %rax
je L28
# | ((int8*)(custom_printf_str)[(int64)(custom_printf_str_idx)] = (int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)])
leaq -550(%rbp), %rax
movq (%rax), %rax
movq -558(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
leaq -16(%rbp), %rbx
movq (%rbx), %rbx
movq -566(%rbp), %rcx
movq $1, %rdx
imulq %rcx, %rdx
addq %rdx, %rbx
movb (%rbx), %bl
movsx %bl, %rbx
movb %bl, (%rax)
# | ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
movq -566(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -566(%rbp)
# | ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + 1))
movq -558(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -558(%rbp)
jmp L27
L28:
# | ((int8)(custom_printf_flag) = 0)
movq $0, %rax
movb %al, -41(%rbp)
# | ((int8)(custom_printf_repeat) = 1)
movq $1, %rax
movb %al, -42(%rbp)
# | while (widen((int8)(custom_printf_repeat)) == 1)
# |   ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |   if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('-'))
# |     ((int8)(custom_printf_flag) = (int8)(minus_flag))
# |   else
# |         if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('0'))
# |       ((int8)(custom_printf_flag) = (int8)(zero_flag))
# |     else
# |             if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('+'))
# |         ((int8)(custom_printf_flag) = (int8)(plus_flag))
# |       else
# |                 if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen(' '))
# |           ((int8)(custom_printf_flag) = (int8)(space_flag))
# |         else
# |           ((int8)(custom_printf_repeat) = 0)
# |         end
# |       end
# |     end
# |   end
L29:
movb -42(%rbp), %al
movsx %al, %rax
movq $1, %rbx
cmp %rbx, %rax
jne L30
# | ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
movq -566(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -566(%rbp)
# | if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('-'))
# |   ((int8)(custom_printf_flag) = (int8)(minus_flag))
# | else
# |     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('0'))
# |     ((int8)(custom_printf_flag) = (int8)(zero_flag))
# |   else
# |         if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('+'))
# |       ((int8)(custom_printf_flag) = (int8)(plus_flag))
# |     else
# |             if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen(' '))
# |         ((int8)(custom_printf_flag) = (int8)(space_flag))
# |       else
# |         ((int8)(custom_printf_repeat) = 0)
# |       end
# |     end
# |   end
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $45, %bl
movsx %bl, %rbx
cmp %rbx, %rax
jne L31
# | ((int8)(custom_printf_flag) = (int8)(minus_flag))
movb minus_flag(%rip), %al
movb %al, -41(%rbp)
jmp L32
L31:
# | if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('0'))
# |   ((int8)(custom_printf_flag) = (int8)(zero_flag))
# | else
# |     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('+'))
# |     ((int8)(custom_printf_flag) = (int8)(plus_flag))
# |   else
# |         if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen(' '))
# |       ((int8)(custom_printf_flag) = (int8)(space_flag))
# |     else
# |       ((int8)(custom_printf_repeat) = 0)
# |     end
# |   end
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $48, %bl
movsx %bl, %rbx
cmp %rbx, %rax
jne L33
# | ((int8)(custom_printf_flag) = (int8)(zero_flag))
movb zero_flag(%rip), %al
movb %al, -41(%rbp)
jmp L34
L33:
# | if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('+'))
# |   ((int8)(custom_printf_flag) = (int8)(plus_flag))
# | else
# |     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen(' '))
# |     ((int8)(custom_printf_flag) = (int8)(space_flag))
# |   else
# |     ((int8)(custom_printf_repeat) = 0)
# |   end
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $43, %bl
movsx %bl, %rbx
cmp %rbx, %rax
jne L35
# | ((int8)(custom_printf_flag) = (int8)(plus_flag))
movb plus_flag(%rip), %al
movb %al, -41(%rbp)
jmp L36
L35:
# | if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen(' '))
# |   ((int8)(custom_printf_flag) = (int8)(space_flag))
# | else
# |   ((int8)(custom_printf_repeat) = 0)
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $32, %bl
movsx %bl, %rbx
cmp %rbx, %rax
jne L37
# | ((int8)(custom_printf_flag) = (int8)(space_flag))
movb space_flag(%rip), %al
movb %al, -41(%rbp)
jmp L38
L37:
# | ((int8)(custom_printf_repeat) = 0)
movq $0, %rax
movb %al, -42(%rbp)
L38:
L36:
L34:
L32:
jmp L29
L30:
# | ((int64)(custom_printf_width) = 0)
movq $0, %rax
movq %rax, -574(%rbp)
# | if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('*'))
# |   ((int64)(custom_printf_width) = va_arg((int64[3])(custom_printf_va_list)))
# | else
# |     ((int64)(custom_printf_cnt) = 0)
# |   while (widen(isdigit((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)])) > 0)
# |     ((int64)(custom_printf_cnt) = ((int64)(custom_printf_cnt) + 1))
# |     ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
# |   end
# |   if ((int64)(custom_printf_cnt) > 0)
# |     ((int64)(custom_printf_width) = strnToU64(cast("void*", (cast("int64", cast("void*", (cast("int64", (int8*)(custom_printf_format)) + (int64)(custom_printf_format_idx)))) - (int64)(custom_printf_cnt))), (int64)(custom_printf_cnt)))
# |   end
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $42, %bl
movsx %bl, %rbx
cmp %rbx, %rax
jne L39
# | ((int64)(custom_printf_width) = va_arg((int64[3])(custom_printf_va_list)))
# | va_arg((int64[3])(custom_printf_va_list))
leaq -40(%rbp), %rax
movq %rax, %rdi
call va_arg
movq %rax, -574(%rbp)
jmp L40
L39:
# | ((int64)(custom_printf_cnt) = 0)
movq $0, %rax
movq %rax, -582(%rbp)
# | while (widen(isdigit((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)])) > 0)
# |   ((int64)(custom_printf_cnt) = ((int64)(custom_printf_cnt) + 1))
# |   ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
L41:
# | isdigit((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)])
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movq %rax, %rdi
call isdigit
movq $0, %rbx
cmp %rbx, %rax
jle L42
# | ((int64)(custom_printf_cnt) = ((int64)(custom_printf_cnt) + 1))
movq -582(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -582(%rbp)
# | ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
movq -566(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -566(%rbp)
jmp L41
L42:
# | if ((int64)(custom_printf_cnt) > 0)
# |   ((int64)(custom_printf_width) = strnToU64(cast("void*", (cast("int64", cast("void*", (cast("int64", (int8*)(custom_printf_format)) + (int64)(custom_printf_format_idx)))) - (int64)(custom_printf_cnt))), (int64)(custom_printf_cnt)))
movq -582(%rbp), %rbx
movq $0, %rax
cmp %rax, %rbx
jle L43
# | ((int64)(custom_printf_width) = strnToU64(cast("void*", (cast("int64", cast("void*", (cast("int64", (int8*)(custom_printf_format)) + (int64)(custom_printf_format_idx)))) - (int64)(custom_printf_cnt))), (int64)(custom_printf_cnt)))
# | strnToU64(cast("void*", (cast("int64", cast("void*", (cast("int64", (int8*)(custom_printf_format)) + (int64)(custom_printf_format_idx)))) - (int64)(custom_printf_cnt))), (int64)(custom_printf_cnt))
movq -582(%rbp), %rax
movq %rax, %rsi
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
addq %rbx, %rax
movq -582(%rbp), %rbx
subq %rbx, %rax
movq %rax, %rdi
call strnToU64
movq %rax, -574(%rbp)
L43:
L40:
# | if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('%'))
# |     ((int8*)(custom_printf_str)[(int64)(custom_printf_str_idx)] = widen('%'))
# |   ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + 1))
# | else
# |     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('s'))
# |         ((int8*)(custom_printf_buf) = cast("int8*", va_arg((int64[3])(custom_printf_va_list))))
# |     strcpy(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int8*)(custom_printf_buf))
# |     ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + strlen((int8*)(custom_printf_buf))))
# |   else
# |         if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))
# |             ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |       ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |       number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# |     else
# |             if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('u'))
# |                 ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |         ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |         number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# |       end
# |     end
# |   end
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $37, %bl
movsx %bl, %rbx
cmp %rbx, %rax
jne L44
# | ((int8*)(custom_printf_str)[(int64)(custom_printf_str_idx)] = widen('%'))
leaq -550(%rbp), %rax
movq (%rax), %rax
movq -558(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb $37, %bl
movsx %bl, %rbx
movb %bl, (%rax)
# | ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + 1))
movq -558(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -558(%rbp)
jmp L45
L44:
# | if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('s'))
# |     ((int8*)(custom_printf_buf) = cast("int8*", va_arg((int64[3])(custom_printf_va_list))))
# |   strcpy(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int8*)(custom_printf_buf))
# |   ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + strlen((int8*)(custom_printf_buf))))
# | else
# |     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))
# |         ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |     ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |     number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# |   else
# |         if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('u'))
# |             ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |       ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |       number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# |     end
# |   end
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $115, %bl
movsx %bl, %rbx
cmp %rbx, %rax
jne L46
# | ((int8*)(custom_printf_buf) = cast("int8*", va_arg((int64[3])(custom_printf_va_list))))
# | va_arg((int64[3])(custom_printf_va_list))
leaq -40(%rbp), %rax
movq %rax, %rdi
call va_arg
leaq -590(%rbp), %rbx
movq %rax, (%rbx)
# | strcpy(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int8*)(custom_printf_buf))
leaq -590(%rbp), %rax
movq (%rax), %rax
movq %rax, %rsi
leaq -550(%rbp), %rax
movq (%rax), %rax
movq -558(%rbp), %rbx
addq %rbx, %rax
movq %rax, %rdi
call strcpy
# | ((int64)(custom_printf_str_idx) = ((int64)(custom_printf_str_idx) + strlen((int8*)(custom_printf_buf))))
# | strlen((int8*)(custom_printf_buf))
leaq -590(%rbp), %rax
movq (%rax), %rax
movq %rax, %rdi
call strlen
movq -558(%rbp), %rbx
addq %rax, %rbx
movq %rbx, -558(%rbp)
jmp L47
L46:
# | if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))
# |     ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |   ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |   number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# | else
# |     if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('u'))
# |         ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |     ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |     number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
# |   end
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $100, %bl
movsx %bl, %rbx
cmp %rbx, %rax
jne L48
# | ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $100, %bl
movsx %bl, %rbx
cmp %rbx, %rax
sete %al
movb %al, -600(%rbp)
# | ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# | va_arg((int64[3])(custom_printf_va_list))
leaq -40(%rbp), %rax
movq %rax, %rdi
call va_arg
movq %rax, -608(%rbp)
# | number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
movq -574(%rbp), %rax
movq %rax, %r8
movb -41(%rbp), %al
movb %al, %cl
movb -600(%rbp), %al
movb %al, %dl
movq -608(%rbp), %rax
movq %rax, %rsi
leaq -550(%rbp), %rax
movq (%rax), %rax
movq -558(%rbp), %rbx
addq %rbx, %rax
movq %rax, %rdi
call number
jmp L49
L48:
# | if ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('u'))
# |     ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
# |   ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# |   number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $117, %bl
movsx %bl, %rbx
cmp %rbx, %rax
jne L50
# | ((int8)(custom_printf_repr) = cast("int8", ((int8*)(custom_printf_format)[(int64)(custom_printf_format_idx)] == widen('d'))))
leaq -16(%rbp), %rax
movq (%rax), %rax
movq -566(%rbp), %rbx
movq $1, %rcx
imulq %rbx, %rcx
addq %rcx, %rax
movb (%rax), %al
movsx %al, %rax
movb $100, %bl
movsx %bl, %rbx
cmp %rbx, %rax
sete %al
movb %al, -600(%rbp)
# | ((int64)(custom_printf_num) = va_arg((int64[3])(custom_printf_va_list)))
# | va_arg((int64[3])(custom_printf_va_list))
leaq -40(%rbp), %rax
movq %rax, %rdi
call va_arg
movq %rax, -608(%rbp)
# | number(cast("void*", (cast("int64", (int8*)(custom_printf_str)) + (int64)(custom_printf_str_idx))), (int64)(custom_printf_num), (int8)(custom_printf_repr), (int8)(custom_printf_flag), (int64)(custom_printf_width))
movq -574(%rbp), %rax
movq %rax, %r8
movb -41(%rbp), %al
movb %al, %cl
movb -600(%rbp), %al
movb %al, %dl
movq -608(%rbp), %rax
movq %rax, %rsi
leaq -550(%rbp), %rax
movq (%rax), %rax
movq -558(%rbp), %rbx
addq %rbx, %rax
movq %rax, %rdi
call number
L50:
L49:
L47:
L45:
# | ((int64)(custom_printf_format_idx) = ((int64)(custom_printf_format_idx) + 1))
movq -566(%rbp), %rbx
movq $1, %rax
addq %rax, %rbx
movq %rbx, -566(%rbp)
jmp L25
L26:
# | puts((int8[500])(custom_printf_arr))
leaq -542(%rbp), %rax
movq %rax, %rdi
call puts
# | _va_end((int64[3])(custom_printf_va_list))
leaq -40(%rbp), %rax
movq %rax, %rdi
call _va_end
leave
ret
# | main_repr: -9(%rbp)
# | main_flag: -10(%rbp)
# | main_num: -18(%rbp)
# | main_width: -26(%rbp)
# | main_buff: -76(%rbp)
# | main_fmt: -84(%rbp)
# | fun main()
# |   ((int8)(main_repr) = 1)
# |   ((int8)(main_flag) = 2)
# |   ((int64)(main_num) = (0 - 150))
# |   ((int64)(main_width) = 0)
# |   ((int8*)(main_fmt) = "Message: %s %d")
# |   custom_printf((int8*)(main_fmt), "Hello world", 16)
# |   ret 0
main:
push %rbp
mov %rsp, %rbp
sub $96, %rsp
# | ((int8)(main_repr) = 1)
movq $1, %rax
movb %al, -9(%rbp)
# | ((int8)(main_flag) = 2)
movq $2, %rax
movb %al, -10(%rbp)
# | ((int64)(main_num) = (0 - 150))
movq $0, %rax
movq $150, %rbx
subq %rbx, %rax
movq %rax, -18(%rbp)
# | ((int64)(main_width) = 0)
movq $0, %rax
movq %rax, -26(%rbp)
# | ((int8*)(main_fmt) = "Message: %s %d")
leaq str_2(%rip), %rax
leaq -84(%rbp), %rbx
movq %rax, (%rbx)
# | custom_printf((int8*)(main_fmt), "Hello world", 16)
movq $16, %rax
movq %rax, %rdx
leaq str_3(%rip), %rax
movq %rax, %rsi
leaq -84(%rbp), %rax
movq (%rax), %rax
movq %rax, %rdi
xor %rax, %rax
call custom_printf
# | ret 0
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
.extern strdup
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
.extern fopen
.extern fclose
.extern fread
.extern fwrite
.extern fseek
.extern ftell
.extern rewind
.extern remove
.extern rename
.global U64ToStrLen
.global U64ToStr
.global strnToU64
.global number
.global _va_start
.global _va_end
.global va_arg
.global custom_printf
.global main

.data
str_0: .asciz "number before width"
str_1: .asciz "number after width"
str_2: .asciz "Message: %s %d"
str_3: .asciz "Hello world"
mzf_mask: .byte 12
minus_flag: .byte 8
zero_flag: .byte 4
plus_flag: .byte 2
space_flag: .byte 1
