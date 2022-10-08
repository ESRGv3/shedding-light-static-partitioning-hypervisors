#! /bin/sh

modprobe jailhouse && jailhouse enable jailhouse/root.cell
jailhouse cell create jailhouse/irqstorm.cell && jailhouse cell load 1 jailhouse/irqstorm.bin -a 0x40000000 && jailhouse cell start 1 
