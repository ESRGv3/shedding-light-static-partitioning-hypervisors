## Build


```
# cd $(SHEDLIGHT)xen/xen/xen
# export XEN_TARGET_ARCH=arm64 CROSS_COMPILE=aarch64-none-elf-
# cp ../../xen-minimal-config .config && make oldconfig
```

Note that you will need to manually enable/disable the CONFIG_CACHE_COLORING
option, according to the config your using. This is because if cache colorig
is enabled in Kconfig but is not actually used (lets say you assign all colors
to all domains and hypervisor), the hypervisor will still use 4K pages for all
domain mappings, causing a noticeable impact for the base case benchamrk.

### Install

The steps that build the configurations using image builder and install the hypervisor, guest
images and the u-boot scripts in the sd card are automated in the Makefile next to this readme.
Run `make CONFIG=$TARGET_CONFIG install` so that it installs it in your sdcard according to
top-level readme. $TARGET_CONFIG is the name of one of the directories in *configs*.

## Run

Run the following command in the u-boot prompt:

```
fatload mmc 0 0 xen.scr && source 0
```       



