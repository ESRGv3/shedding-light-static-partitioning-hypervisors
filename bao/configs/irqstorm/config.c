#include <config.h>

VM_IMAGE(irqlat, "../../guests/irqstorm/build/zcu104/baremetal.bin");

struct config config = { 
     
    CONFIG_HEADER
    
    .vmlist_size = 1,
    .vmlist = {
        { 

            .entry = 0x40000000,

            .image = {
                .base_addr = 0x40000000,
                .load_addr = VM_IMAGE_OFFSET(irqlat),
                .size = VM_IMAGE_SIZE(irqlat)
            },

            .cpu_affinity = 0b1000,
            // .direct_injection = true,

            .platform = {
                .cpu_num = 1,
                
                .region_num = 1,
                .regions =  (struct mem_region[]) {
                    {
                        .base = 0x40000000,
                        .size = 0x8000000
                    }
                },

                .dev_num = 3,
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
                    },
                    {   
                        /* interrupter */
                        .pa = 0xa0000000,
                        .va = 0xa0000000,
                        .size = 0x1000,
                        .interrupt_num = 16,
                        .interrupts =  (irqid_t[]) {121,122,123,124,125,126,127,128,136,137,138,139,140,141,142,143}                         
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
    }
};
