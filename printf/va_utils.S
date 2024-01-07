.text

/*
	// Minimalistic va_list implementation
	// There's no way to rewind va_list (just as Stallman intended)
	struct va_list
	{
		uint64 arg_i;
		void* reg_param_ptr; // Saved by caller (printf)
		void* stack_param_ptr; // Saved by caller's caller (main)
	};
*/

# @brief Calculates the rsp offset from 2 base pointers (rbp_fun, rbp_parent)
# @param callee_rbp Represents the rbp of the function (rbp_fun)
# @param caller_rbp Represents the rbp of the parent function (rbp_parent)
.macro get_caller_rsp_off callee_rbp, caller_rbp
	mov \caller_rbp, %rax
	mov \callee_rbp, %rcx
	sub %rcx, %rax
.endm

# Push values in reverse order
.macro stack_snapshot
	push %r9
	push %r8
	push %rcx
	push %rdx
	push %rsi
	push %rdi
.endm

# main: mov $0, %rdi; mov $1, %rax; push $24; push $25; call fun (rsp_old_old)
# fun: push %rdi; push %rsi; va_list(24bytes); call va_start (rsp_old)
# vs_start: %rdi (rsp)

.macro stack_snapsot_rewind
	pop %rdi
	pop %rsi
	pop %rdx
	pop %rcx
	pop %r8
	pop %r9
.endm


.global _va_start
.global _va_arg

_va_start:

	# @param rdi- va_list (void*)

	push %rbp
	mov %rsp, %rbp

	movq $0, (%rdi)

	# reg_param_ptr
	mov (%rbp), %rdx # rdx = rbp_old
	get_caller_rsp_off %rbp, %rdx # rax = rsp_off
	add $16, %rdx # skip caller's return addr and rbp
	sub %rax, %rdx # add rsp_off, rdx = rsp_old
	mov %rdx, 8(%rdi) # va_list.reg_param_ptr = rdx = rsp_old

	# stack_param_ptr (rdx)
	mov (%rbp), %rax # rax = rbp_old
	mov (%rax), %rdx # rdx = *rax = rbp_old_old
	get_caller_rsp_off (%rbp), %rdx
	add $16, %rdx # skip caller's caller return addr and rbp
	sub %rax, %rdx
	mov %rdx, 16(%rdi)

	leave
	ret

_va_arg:

	push %rbp
	mov %rsp, %rbp

	# @param rdi - va_list (void*)
	# @return the requested arg (uint64)

	cmpq $6, (%rdi)
	jge stack_alloc
	mov 8(%rdi), %rbx
	mov (%rdi), %rcx
	jmp _va_arg_end
	stack_alloc:
	mov 16(%rdi), %rbx
	mov (%rdi), %rcx
	sub $6, %rcx

	_va_arg_end:
	mov (%rbx, %rcx, 8), %rax
	incq (%rdi)

	leave
	ret