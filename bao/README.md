# Bao

# Build

```
# cd $SHEDLIGHT/bao/bao
# make PLATFORM=zcu104 CONFIG_BUILTIN=y CONFIG_REPO=$SHEDLIGHT/bao/configs/$CONFIG
# cp bin/zcu104/builtin-configs/$CONFIG/bao.bin $SHEDLIGHT/install/boot
```

## Install

Copy all files $SHEDLIGHT/install/boot to your $SDCARD_BOOT.

```
# cp $SHEDLIGHT/install/boot/* $SDCARD_BOOT
```

## Run

Reset the board. On u-boot prompt:

```
# fatload mmc 0 0x200000 bao.bin; go 0x200000
```
