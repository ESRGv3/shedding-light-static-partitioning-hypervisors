#! /bin/sh

modprobe jailhouse && jailhouse enable jailhouse/root.cell
jailhouse cell create jailhouse/tx.cell && jailhouse cell load 1 jailhouse/transfer-tx.bin -a 0x40000000 && jailhouse cell start 1
jailhouse cell create jailhouse/rx.cell && jailhouse cell load 2 jailhouse/transfer-rx.bin -a 0x40000000 && jailhouse cell start 2
