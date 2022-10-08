#include <config.h>

VM_IMAGE(linux, "../lloader/linux.bin");

struct config config = { 
     
    CONFIG_HEADER
    
    .vmlist_size = 1,
    .vmlist = {
        { 

            .entry = 0x40000000,

            .image = {
                .base_addr = 0x40000000,
                .load_addr = VM_IMAGE_OFFSET(linux),
                .size = VM_IMAGE_SIZE(linux),
            },

            .cpu_affinity = 0b1000,

            .platform = {
                .cpu_num = 1,
                
                .region_num = 1,
                .regions =  (struct mem_region[]) { 
                    {
                        .base = 0x40000000,
                        .size = 0x10000000, //512MB
                    }
                },

                .dev_num = 2,
                .devs =  (struct dev_region[]) {
                    {   
                        /* UART */
                        .pa = 0xFF010000,
                        .va = 0xFF010000,
                        .size = 0x1000,
                        .interrupt_num = 1,
                        .interrupts = 
                            (irqid_t[]) {54}                         
                    },
                    {   
                        /* Arch timer interrupt */
                        .interrupt_num = 1,
                        .interrupts = 
                            (irqid_t[]) {27}                         
                    },
                },

                .arch = {
                    .gic = {
                        .gicc_addr = 0xF902f000,
                        .gicd_addr = 0xF9010000
                    },
                }
            },
        },
    }
};
