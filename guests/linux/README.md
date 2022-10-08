# Buildroot rootfs

```
# cd $SHEDLIGHT/guests/linux
# git clone https://github.com/buildroot/buildroot.git --depth 1 --branch 2021.08.1
# cd buildroot
# make qemu_aarch64_virt_defconfig
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

Finally run `make`.

# Linux kernel

```
# cd $SHEDLIGHT/guests/linux
# git clone https://github.com/torvalds/linux.git --depth 1 --branch v5.14
# cd linux
# export ARCH=arm64 CROSS_COMPILE=$SHEDLIGHT/guests/linux/buildroot/output/bin/aarch64-linux-
# make defconfig
```

For the guest Linux we build it with a built-in ramfs cpio.
Set the following kconfig options (e.g. in the `make menuconfig` menu):

- CONFIG_DRM=n
- CONFIG_INITRAMFS_SOURCE=*`$SHEDLIGHT`/guests/linux/buildroot/output/images/rootfs.cpio*

And run:
```
# make -j$(ncpu) Image
```

# Add benchmark tools to rootfs

Now we need to incorporate a couple of tools for benchmarking in the rootfs. 
Create a rootfs overlay directory:

```
mkdir -p $SHEDLIGHT/guests/linux/rootfs-overlay/root
```

Build and copy perf executable in *tools/perf* to the rootfs overlay:

```
cd $SHEDLIGHT/guests/linux/linux/tools/perf/
export ARCH=arm64 CROSS_COMPILE=$SHEDLIGHT/guests/linux/buildroot/output/bin/aarch64-linux-
make
cp perf $SHEDLIGHT/guests/linux/rootfs-overlay/root/
```

Go to the mibench benchmark dir, build it, and copy it to the rootfs:

```
cd $SHEDLIGHT/guests/linux/mibench
export ARCH=arm64 CROSS_COMPILE=$SHEDLIGHT/guests/linux/buildroot/output/bin/aarch64-linux-
make
cp -r $SHEDLIGHT/guests/linux/mibench $SHEDLIGHT/guests/linux/rootfs-overlay/root/
```

Finnaly go back to the buildroot directory and rebuilt it to incroporate the overlay in
the final rootfs:

```
cd $SHEDLIGHT/guests/linux/buildroot
make menuconfig
```

Add:
- BR2_PACKAGE_ROOTFS_OVERLAY=$SHEDLIGHT/guests/linux/rootfs-overlay/

And rebuild buildroot: `make`

Finally rebuild Linux to incorporate the final rootfs:

```
cd $SHEDLIGHT/guests/linux/linux
make -j$(nproc) Image
```
