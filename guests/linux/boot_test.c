#include <stdio.h>
#include <stdint.h>

int main() {

    uint64_t counter = 0;
    asm volatile("mrs %0, CNTPCT_EL0" : "=r"(counter));
    printf("boottime-linux %lu\n", counter);
    
    while(1);
    return 0;
}

