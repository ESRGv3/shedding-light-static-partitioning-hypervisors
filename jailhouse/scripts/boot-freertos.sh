#! /bin/sh

modprobe jailhouse && jailhouse enable /root/jailhouse/root.cell
jailhouse cell create /root/jailhouse/freertos.cell && jailhouse cell load 1 /root/jailhouse/freertos.bin -a 0x40000000 && jailhouse cell start 1
