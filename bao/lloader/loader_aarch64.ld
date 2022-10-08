ENTRY(_start)

SECTIONS
{   
    .nloader : {
        KEEP(*(.nloader))
    }

    .dtb 0x80000 : { 
        __dtb_start = ABSOLUTE(.);
        KEEP(*(.dtb)) 
        __dtb_end = .;
    }  
    
    .linux 0x200000 : { 
        __linux_start = .;
        KEEP(*(.linux)) 
        __linux_end = .;
    }  
}
