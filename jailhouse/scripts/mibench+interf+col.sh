#! /bin/sh

modprobe jailhouse && jailhouse enable jailhouse/root.cell
jailhouse cell create jailhouse/interf+col.cell && jailhouse cell load 1 jailhouse/interf.bin -a 0x40000000 && jailhouse cell start 1
jailhouse cell linux jailhouse/linux+col.cell jailhouse/Image -d jailhouse/linux.dtb -c "console=ttyPS0,115200"

