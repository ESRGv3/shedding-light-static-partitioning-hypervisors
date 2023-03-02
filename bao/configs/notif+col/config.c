#include <config.h>

VM_IMAGE(tx, "../../guests/comm/notif/tx/build/zcu104-BAO/baremetal.bin");
VM_IMAGE(rx, "../../guests/comm/notif/rx/build/zcu104-BAO/baremetal.bin");

#define SHMEM_BASE (0x30000000)
#define SHMEM_SIZE ((16 * 1024 * 1024) + 0x1000)

struct config config = { 
     
    CONFIG_HEADER
    
    .shmemlist_size =  1,
    .shmemlist = (struct shmem[]) {
        {
            .size = SHMEM_SIZE,
            // .place_phys = true,
            // .phys = SHMEM_BASE - SHMEM_SIZE,
            .colors = 0b00001111,
        }
    },

    .vmlist_size = 2,
    .vmlist = {
        { 

            .entry = 0x40000000,

            .image = {
                .base_addr = 0x40000000,
                .load_addr = VM_IMAGE_OFFSET(tx),
                .size = VM_IMAGE_SIZE(tx),
            },

            .cpu_affinity = 0b1000,
            .colors = 0b00001111,

            .platform = {
                .cpu_num = 1,
                
                .region_num = 1,
                .regions =  (struct mem_region[]) {
                    {
                        .base = 0x40000000,
                        .size = 0x8000000,
                    }
                },

                .ipc_num = 1,
                .ipcs = (struct ipc[]) {
                    {
                        .shmem_id = 0,
                        .base = SHMEM_BASE,
                        .size = SHMEM_SIZE,
                        .interrupt_num = 1,
                        .interrupts = (irqid_t[]) { 96 }
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
                .load_addr = VM_IMAGE_OFFSET(rx),
                .size = VM_IMAGE_SIZE(rx),
            },
            .colors = 0b00001111,

            .cpu_affinity = 0b0100,

            .platform = {
                .cpu_num = 1,
                
                .region_num = 1,
                .regions =  (struct mem_region[]) {
                    {
                        .base = 0x40000000,
                        .size = 0x8000000,
                    }
                },


                .ipc_num = 1,
                .ipcs = (struct ipc[]) {
                    {
                        .shmem_id = 0,
                        .base = SHMEM_BASE,
                        .size = SHMEM_SIZE,
                        .interrupt_num = 1,
                        .interrupts = (irqid_t[]) { 96 }
                    }
                },


                .dev_num = 2,
                .devs =  (struct dev_region[]) {
                    {   
                        /* UART 1 */
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
