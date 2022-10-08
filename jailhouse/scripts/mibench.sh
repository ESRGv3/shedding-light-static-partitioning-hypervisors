#! /bin/sh

modprobe jailhouse && jailhouse enable jailhouse/root.cell
jailhouse cell linux jailhouse/linux.cell jailhouse/Image -d jailhouse/linux.dtb -c "console=ttyPS0,115200" #nohz_full=3
