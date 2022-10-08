#include <stdio.h>
#include <stdint.h>

int main() {
   
    //printf("hello from userspace\n"); 

    uint64_t counter = 0;
    asm volatile("mrs %0, CNTPCT_EL0" : "=r"(counter));
    printf("boottime-user %lu\n", counter);
    
    while(1);
    return 0;
}

