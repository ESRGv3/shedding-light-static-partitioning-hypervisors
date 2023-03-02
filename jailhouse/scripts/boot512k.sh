#! /bin/sh

modprobe jailhouse && jailhouse enable /root/jailhouse/root.cell
jailhouse cell create /root/jailhouse/boot.cell && jailhouse cell load 1 /root/jailhouse/boot512k.bin -a 0x40000000 && jailhouse cell start 1 
