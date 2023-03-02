#! /bin/sh

modprobe jailhouse && jailhouse enable jailhouse/root.cell
jailhouse cell create jailhouse/interf.cell && jailhouse cell load 1 jailhouse/interf2.bin -a 0x40000000 && jailhouse cell start 1
jailhouse cell create jailhouse/irqlat.cell && jailhouse cell load 2 jailhouse/irqlat.bin -a 0x40000000 && jailhouse cell start 2
