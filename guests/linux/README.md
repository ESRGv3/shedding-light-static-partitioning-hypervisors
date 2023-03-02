# Buildroot rootfs

```
# cd $SHEDLIGHT/guests/linux
# git clone https://github.com/buildroot/buildroot.git --depth 1 --branch 2021.08.1
# cd buildroot
# make qemu_aarch64_virt_defconfig
```

Create a rootfs overlay directory:

```
# mkdir -p $SHEDLIGHT/guests/linux/rootfs-overlay/bin
# mkdir -p $SHEDLIGHT/guests/linux/rootfs-overlay/root
```

Then set the following kconfig options (e.g. in the `make menuconfig` menu):

- BR2_LINUX_KERNEL=n
- BR2_TOOLCHAIN_BUILDROOT_GLIBC=y
- BR2_PACKAGE_LIBZLIB
- BR2_SYSTEM_DHCP=
- BR2_TARGET_GENERIC_GETTY_PORT=console
- BR2_TARGET_ROOTFS_EXT2=n
- BR2_TARGET_ROOTFS_CPIO=y
- BR2_PACKAGE_HOST_QEMU=n
- BR2_ROOTFS_OVERLAY=$SHEDLIGHT/guests/linux/rootfs-overlay/

Finally run `make`.

# Linux kernel

```
# cd $SHEDLIGHT/guests/linux
# git clone https://github.com/torvalds/linux.git --depth 1 --branch v5.14
# cd linux
# git am $SHEDLIGHT/guests/linux/0001-allow-user-access-to-timer.patch
# export ARCH=arm64 CROSS_COMPILE=$SHEDLIGHT/guests/linux/buildroot/output/host/bin/aarch64-linux-
# make defconfig
```

For the guest Linux we build it with a built-in ramfs cpio.
Set the following kconfig options (e.g. in the `make menuconfig` menu):

- CONFIG_INITRAMFS_SOURCE=*`$SHEDLIGHT`/guests/linux/buildroot/output/images/rootfs.cpio*

And run:
```
# make -j$(ncpu) Image
```

# Add benchmark tools to rootfs

Now we need to incorporate a couple of tools for benchmarking in the rootfs. 
Build and copy perf executable in *tools/perf* to the rootfs overlay:

```
# cd $SHEDLIGHT/guests/linux/linux/tools/perf/
# export ARCH=arm64 CROSS_COMPILE=$SHEDLIGHT/guests/linux/buildroot/output/host/bin/aarch64-linux-
# make
# cp perf $SHEDLIGHT/guests/linux/rootfs-overlay/bin/
```

Go to the mibench benchmark dir, build it, and copy it to the rootfs:

```
# cd $SHEDLIGHT/guests/linux/mibench
# ARCH=arm64 CROSS_COMPILE=$SHEDLIGHT/guests/linux/buildroot/output/host/bin/aarch64-linux- \
    make
# cp -r $SHEDLIGHT/guests/linux/mibench $SHEDLIGHT/guests/linux/rootfs-overlay/root/
```

Build the boot test:

```
# cd $SHEDLIGHT/guests/linux/
# $SHEDLIGHT/guests/linux/buildroot/output/host/bin/aarch64-linux-gcc boot_test.c -o boot_test
# cp boot_test $SHEDLIGHT/guests/linux/rootfs-overlay/root/
```

Re-build the rootfs to incroporate the new additions to the overlay in
the final rootfs, and rebuild the Linux Image to incorporate the new rootfs:

```
# make -C $SHEDLIGHT/guests/linux/buildroot
# ARCH=arm64 CROSS_COMPILE=$SHEDLIGHT/guests/linux/buildroot/output/host/bin/aarch64-linux- \
    make -C $SHEDLIGHT/guests/linux/linux -j$(nproc) Image
```

Finally, compile Linux's device tree and wrapper (needs will be need it to run it
baremetal and over bao:

```
# cd $SHEDLIGHT/guests/linux/
# dtc linux.dts -o linux.dtb
# cd $SHEDLIGHT/guests/linux/lloader
# make ARCH=aarch64 IMAGE=../linux/arch/arm64/boot/Image DTB=../linux.dtb TARGET=linux
```

Also repeat this for the boot test image:

```
# cd $SHEDLIGHT/guests/linux/
# dtc linux-boot.dts -o linux-boot.dtb
# cd $SHEDLIGHT/guests/linux/lloader
# make ARCH=aarch64 IMAGE=../linux/arch/arm64/boot/Image DTB=../linux-boot.dtb TARGET=linux-boot
```

