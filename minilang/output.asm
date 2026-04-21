default rel
global main
extern printf

section .text
main:
    push rbp
    mov rbp, rsp

    mov rax, 10
    mov [x], rax
    mov rax, [x]
    mov rcx, 2
    imul rax, rcx
    mov [t1], rax
    mov rax, [t1]
    mov rcx, 5
    add rax, rcx
    mov [t2], rax
    mov rax, [t2]
    mov [y], rax
    mov rax, [y]
    mov rcx, 20
    cmp rax, rcx
    setg al
    movzx rax, al
    mov [t3], rax
    mov rax, [t3]
    cmp rax, 0
    je L1
    sub rsp, 32
    mov rdx, [y]
    lea rcx, [fmt]
    xor eax, eax
    call printf
    add rsp, 32
L1:
    mov eax, 0
    pop rbp
    ret

section .data
fmt db "%d", 10, 0

section .bss
t2 resq 1
y resq 1
t1 resq 1
x resq 1
t3 resq 1