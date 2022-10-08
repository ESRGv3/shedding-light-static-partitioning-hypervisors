# Bao

## Build and Installation

All build and instalation steps are automated in the Makefile next to this
readme. It install the hypervisor and guest images in the sd card are automated
in the Makefile next to this readme. Run `make CONFIG=$TARGET_CONFIG install`
so that it installs it in your sdcard according to top-level readme.
$TARGET_CONFIG is the name of one of the directories in *configs*.

## Run

Reset the board. On u-boot prompt:

```
# fatload mmc 0 0x200000 bao.bin; go 0x200000
```
