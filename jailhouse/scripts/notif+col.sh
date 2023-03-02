#! /bin/sh

modprobe jailhouse && jailhouse enable jailhouse/root.cell
jailhouse cell create jailhouse/tx+col.cell && jailhouse cell load 1 jailhouse/notif-tx.bin -a 0x40000000 && jailhouse cell start 1
jailhouse cell create jailhouse/rx+col.cell && jailhouse cell load 2 jailhouse/notif-rx.bin -a 0x40000000 && jailhouse cell start 2
