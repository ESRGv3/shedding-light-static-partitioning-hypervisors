# Xen

## Config


```
# cd $SHEDLIGHT/xen/xen/xen
# export XEN_TARGET_ARCH=arm64 CROSS_COMPILE=aarch64-none-elf-
# cp ../../xen-minimal-config .config && make oldconfig
```

### Configure Cache Coloring

Note that you will need to manually enable/disable the CONFIG_CACHE_COLORING
option, according to the config your using. This is because if cache colorig
is enabled in Kconfig but is not actually used (lets say you assign all colors
to all domains and hypervisor), the hypervisor will still use 4K pages for all
domain mappings, causing a noticeable impact for the base case benchamrk.

```
# cd $SHEDLIGHT/xen/xen/xen
# XEN_TARGET_ARCH=arm64 make menuconfig
```

Then set the `Architecture Features -> Last Level Cache (LLC) Coloring` 
according to if you need to disable or enable cache coloring.


## Build

```
cd $SHEDLIGHT/xen/xen/xen
# export XEN_TARGET_ARCH=arm64 CROSS_COMPILE=aarch64-none-linux-gnu-
# make -j$(nproc)
```

```
# cd $SHEDLIGHT/xen/imagebuilder
# ./scripts/uboot-script-gen -c $SHEDLIGHT/xen/configs/$CONFIG -d $SHEDLIGHT \
     -t "fatload mmc 0" -i $SHEDLIGHT/install/boot
```

## Install

Copy all files $SHEDLIGHT/install/boot to your $SDCARD_BOOT.

```
# cp $SHEDLIGHT/install/boot/* $SDCARD_BOOT
```

## Run

Insert the sd card in your board and turn it on. Run the following command in 
the u-boot prompt:

```
fatload mmc 0 0 xen.scr && source 0
```



