# Jailhouse

## Build root cell

Create the install directory in Jailhouse's repo:

```
mkdir $SHEDLIGHT/jailhouse/jailhouse/install
```

Then, setup buildroot for building the root cell's file system:

```
# mkdir -p $SHEDLIGHT/jailhouse/rootcell
# cd $SHEDLIGHT/jailhouse/rootcell
# git clone https://github.com/buildroot/buildroot.git --depth 1 --branch 2021.08.1
# cd buildroot
# make qemu_aarch64_virt_defconfig
```

Then set the following kconfig options (e.g. in the `make menuconfig` menu):
- Generic:
    - BR2_LINUX_KERNEL=n
    - BR2_TARGET_GENERIC_GETTY_PORT=console
    - BR2_SYSTEM_DHCP=
    - BR2_TARGET_ROOTFS_EXT2=n
    - BR2_TARGET_ROOTFS_TAR=y
    - BR2_TOOLCHAIN_BUILDROOT_GLIBC=y
    - BR2_PACKAGE_PYTHON3=y
    - BR2_PACKAGE_PYTHON3_ZLIB=y
    - BR2_PACKAGE_HOST_QEMU=n
    - BR2_ROOTFS_OVERLAY=$SHEDLIGHT/jailhouse/jailhouse/install

Then, build it:

```
# make -j$(nproc)
```

Next to the Linux image:

```
# cd $SHEDLIGHT/jailhouse/rootcell
# git clone https://github.com/torvalds/linux.git --depth 1 --branch v5.14
# cd linux
# git am $SHEDLIGHT/jailhouse/0001-export-symbols-needed-by-jailhouse-s-module.patch
# git am $SHEDLIGHT/jailhouse/0001-add-boot-time-instrumentation.patch
# export ARCH=arm64 CROSS_COMPILE=$SHEDLIGHT/jailhouse/rootcell/buildroot/output/host/bin/aarch64-buildroot-linux-gnu-
# make defconfig
```

Then set the following kconfig options (e.g. in the `make menuconfig` menu):
- CONFIG_DRM=n
- CONFIG_NVMEM_ZYNQMP=y
- ARM_SMMU=n
- ARM_SMMU_V3=n

Then build it by running `make -j$(ncpu)`.

## Build Jalhouse

```
# cp $SHEDLIGHT/jailhouse/config.h $SHEDLIGHT/jailhouse/jailhouse/include/jailhouse
# cd $SHEDLIGHT/jailhouse/jailhouse
# make ARCH=arm64 CROSS_COMPILE=aarch64-none-linux-gnu- KDIR=$SHEDLIGHT/dom0-rootcell/linux/ DESTDIR=$(realpath ./install) CONFIG_REPO=../configs install
```

## Install


Rebuild buildroot so that the Jailhouse module installation is added to the rootfs.

```
cd $SHEDLIGHT/jailhouse/rootcell/buildroot
make -j12
```

From this point onward installation in the sd card is automatate by the 
 $SHEDLIGHT/jailhouse/Makefile. The `install-cells` rule install the cells config
and binaries in the sdcards root partition as well as scripts that automate the
running a given configuration. The `install-root` rule automates the copying of
the rootcell image and device tree into the sd cards boot directory referenced
in the top-level readme.

## Run

After starting the board, on u-boot prompt:

```
fatload mmc 0 0x200000 Image && fatload mmc 0 0x1e0000 jailhouse.dtb && booti 0x200000 - 0x1e0000
```

After the root cell booted and you logged in as root (password: root), run the target configuration:
```
# ./jailhouse/scripts/$CONFIG.sh
```
