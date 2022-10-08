#! /bin/sh

modprobe jailhouse && jailhouse enable jailhouse/root.cell
jailhouse cell create jailhouse/irqlat.cell && jailhouse cell load 1 jailhouse/irqlat.bin -a 0x40000000 && jailhouse cell start 1 
