#include <config.h>

VM_IMAGE(linux, "../lloader/linux.bin");
VM_IMAGE(irqlat, "../../guests/irqlat/build/zcu104/baremetal.bin");

struct config config = { 
     
    CONFIG_HEADER

    .hyp_colors = 0b00000001,
    
    .vmlist_size = 2,
    .vmlist = {
        { 

            .entry = 0x40000000,

            .image = {
                .base_addr = 0x40000000,
                .load_addr = VM_IMAGE_OFFSET(irqlat),
                .size = VM_IMAGE_SIZE(irqlat)
            },

            .cpu_affinity = 0b1000,
            .colors = 0b00001110,

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
                        .interrupts =  (uint64_t[]) {54}                         
                    },
                    {   
                        /* Arch timer interrupt */
                        .interrupt_num = 1,
                        .interrupts =  (uint64_t[]) {27}                         
                    },
                    {   
                        /* UART 1 */
                        .pa = 0xFF110000,
                        .va = 0xFF110000,
                        .size = 0x1000,
                        .interrupt_num = 3,
                        .interrupts =  (uint64_t[]) {68,69,70}                         
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
        { 

            .entry = 0x40000000,

            .image = {
                .base_addr = 0x40000000,
                .load_addr = VM_IMAGE_OFFSET(linux),
                .size = VM_IMAGE_SIZE(linux)
            },

            .cpu_affinity = 0b0111,
            .colors = 0b11110000,

            .platform = {
                .cpu_num = 3,
                
                .region_num = 1,
                .regions =  (struct mem_region[]) {
                    {
                        .base = 0x40000000,
                        .size = 0x20000000 //512 MB
                    }
                },

                .dev_num = 2,
                .devs =  (struct dev_region[]) {
                    {   
                        /* UART */
                        .pa = 0xFF000000,
                        .va = 0xFF000000,
                        .size = 0x1000,
                        .interrupt_num = 1,
                        .interrupts = 
                            (/*irqid_t*/uint64_t[]) {53}                         
                    },
                    {   
                        /* Arch timer interrupt */
                        .interrupt_num = 1,
                        .interrupts = 
                            (/*irqid_t*/uint64_t[]) {27}                         
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
