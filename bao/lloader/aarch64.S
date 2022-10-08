#define STRINGIFY2(X) #X
#define STRINGIFY(X) STRINGIFY2(X)

.section .nloader, "a"
.global _start
_start:
    /* Valid Image header.  */
    /* HW reset vector.  */
    b skip_header
    nop

    /* text offset.  */
    .dword 0
    /* image size.  */
    .dword 0
    /* flags.  */
    .dword 8
    /* RES0  */
    .dword 0
    .dword 0
    .dword 0

    /* magic  */
    .dword 0x644d5241
    /* RES0  */
    .dword 0
    /* End of Image header.  */

skip_header:
    /* make sure all exceptions disabled */
    msr daifset, 0xf

    /* make sure mmu disable */
    mrs	x0, sctlr_el1
    mov x1, #1
    bic	x0, x0, x1
    msr	sctlr_el1, x0

    isb

    /* boot protocol */
    adr x0, __dtb_start
    mov x1, xzr
    mov x2, xzr
    mov x3, xzr
    
    /* jump to linux */
    ldr x4, =_start
    ldr x5, =__linux_start
    sub x4, x5, x4
    adr x5, _start
    add x5, x5, x4
    br x5

.section .linux, "a"
    .incbin STRINGIFY(IMAGE)

.section .dtb, "a"
    .incbin STRINGIFY(DTB)
 
