SHEDLIGHT:=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))
INSTALL_BOOT:=$(SHEDLIGHT)/install/boot
INSTALL_ROOT:=$(SHEDLIGHT)/install/root
SDCARD_MOUNT:=/media/$(USER)
SDCARD_BOOT:=$(realpath $(SDCARD_MOUNT)/boot)
SDCARD_ROOT:=$(realpath $(SDCARD_MOUNT)/root)


ifeq ($(CONFIG),)
$(error CONFIG not defined!)
endif

ifneq ($(filter install%sd,$(MAKECMDGOALS)),)
ifeq ($(and $(SDCARD_BOOT),$(SDCARD_ROOT)),)
$(error sd card not inserted)
endif
endif

all:

umount:
	umount $(SDCARD_BOOT) $(SDCARD_ROOT)

install-sd:
	cp -r $(INSTALL_DIR_BOOT)/* $(SDCARD_BOOT)

install-root-sd:
	cp -r $(INSTALL_DIR_ROOT)/* $(SDCARD_ROOT)

.PHONY: umount
