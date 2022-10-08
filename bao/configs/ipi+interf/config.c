#include <config.h>

VM_IMAGE(ipi, "../../guests/ipi/build/zcu104/baremetal.bin");
VM_IMAGE(interf, "../../guests/interf-single/build/zcu104/baremetal.bin");

struct config config = { 
     
    CONFIG_HEADER
    
    .vmlist_size = 2,
    .vmlist = {
        { 

            .entry = 0x40000000,

            .image = {
                .base_addr = 0x40000000,
                .load_addr = VM_IMAGE_OFFSET(ipi),
                .size = VM_IMAGE_SIZE(ipi)
            },

            .cpu_affinity = 0b1100,
            // .direct_injection = true,

            .platform = {
                .cpu_num = 2,
                
                .region_num = 1,
                .regions =  (struct mem_region[]) {
                    {
                        .base = 0x40000000,
                        .size = 0x8000000
                    }
                },

                .dev_num = 2,
                .devs =  (struct dev_region[]) {
                    {       
                        /* UART 1 */
                        .pa = 0xFF010000,
                        .va = 0xFF010000,
                        .size = 0x1000,
                        .interrupt_num = 1,
                        .interrupts =  (irqid_t[]) {54}                         
                    },
                    {   
                        /* Arch timer interrupt */
                        .interrupt_num = 1,
                        .interrupts =  (irqid_t[]) {27}                         
                    }
                },

                .arch = {
                    .gic = {
                        .gicc_addr = 0xF902f000,
                        .gicd_addr = 0xF9010000
                    },
                }
            },
        },
        { 
            .entry = 0x40000000,

            .image = {
                .base_addr = 0x40000000,
                .load_addr = VM_IMAGE_OFFSET(interf),
                .size = VM_IMAGE_SIZE(interf)
            },

            .cpu_affinity = 0b0010,

            .platform = {
                .cpu_num = 1,
                
                .region_num = 1,
                .regions =  (struct mem_region[]) {
                    {
                        .base = 0x40000000,
                        .size = 0x10000000
                    }
                },

                .dev_num = 2,
                .devs =  (struct dev_region[]) {
                    {   
                        /* UART 0 (mapped at uart1) */
                        .pa = 0xFF000000,
                        .va = 0xFF000000,
                        .size = 0x1000,                    
                    },
                    {   
                        /* Arch timer interrupt */
                        .interrupt_num = 1,
                        .interrupts =  (irqid_t[]) {27}                         
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
