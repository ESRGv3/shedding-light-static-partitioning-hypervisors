#! /bin/sh

modprobe jailhouse && jailhouse enable /root/jailhouse/root.cell
jailhouse cell linux /root/jailhouse/linux.cell /root/jailhouse/Image -d /root/jailhouse/linux.dtb -c "console=ttyPS0,115200 rdinit=/root/boot_test" #nohz_full=3
