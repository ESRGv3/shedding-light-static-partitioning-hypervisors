#! /bin/sh

modprobe jailhouse && jailhouse enable jailhouse/root.cell
jailhouse cell create jailhouse/ipi+col.cell && jailhouse cell load 1 jailhouse/ipi.bin -a 0x40000000 && jailhouse cell start 1 
