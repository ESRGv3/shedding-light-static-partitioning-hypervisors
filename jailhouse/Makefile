all: build

CONFIG?=boot128k

include ../setup.mk

jailhouse_dir:=$(realpath jailhouse)
jailhouse_config_header:=$(realpath config.h)
install_dir:=$(jailhouse_dir)/install
configs:=$(realpath configs)
root_kernel_dir:=$(realpath rootcell/linux)
buildroot_dir:=$(realpath rootcell/buildroot/)
buildroot_toolchain:=$(buildroot_dir)/output/host/bin/aarch64-buildroot-linux-gnu-
buildroot_rootfs_tar:=$(buildroot_dir)/output/images/rootfs.tar
rootfs_dir:=$(INSTALL_ROOT)
rootfs_jailhouse_dir:=$(INSTALL_ROOT)/root/jailhouse

build: $(install_dir)

$(install_dir):
	cp $(jailhouse_config_header) $(jailhouse_dir)/include/jailhouse/config.h
	$(MAKE) -C $(jailhouse_dir) ARCH=arm64 CROSS_COMPILE=$(buildroot_toolchain) \
		KDIR=$(root_kernel_dir) DESTDIR=$(install_dir) CONFIG_REPO=$(configs) install

clean:
	$(MAKE) -C $(jailhouse_dir) ARCH=arm64 CROSS_COMPILE=$(buildroot_toolchain) \
		KDIR=$(root_kernel_dir) DESTDIR=$(install_dir) CONFIG_REPO=$(configs) clean

buildroot: build
	$(MAKE) -C $(buildroot_dir)

install-rootfs: buildroot $(rootfs_dir) 
	tar xf $(buildroot_rootfs_tar) --directory=$(rootfs_dir)

install-root: build install-rootfs
	cp $(root_kernel_dir)/arch/arm64/boot/Image $(INSTALL_BOOT)
	cp $(configs)/dts/root.dtb $(INSTALL_BOOT)/jailhouse.dtb	
	cp $(configs)/dts/*.dtb $(INSTALL_BOOT)

install install-cells: build | $(rootfs_jailhouse_dir)
	cp $(configs)/*.cell $(rootfs_jailhouse_dir)
	cp $(configs)/dts/*.dtb $(rootfs_jailhouse_dir)
	-cp $(SHEDLIGHT)/guests/linux/linux/arch/arm64/boot/Image $(rootfs_jailhouse_dir)
	-cp $(SHEDLIGHT)/guests/baremetal/build/zcu104/baremetal.bin $(rootfs_jailhouse_dir)
	-cp $(SHEDLIGHT)/guests/freertos/build/zcu104/freertos.bin $(rootfs_jailhouse_dir)
	-cp $(SHEDLIGHT)/guests/irqlat/build/zcu104/baremetal.bin $(rootfs_jailhouse_dir)/irqlat.bin
	-cp $(SHEDLIGHT)/guests/interf/build/zcu104/baremetal.bin $(rootfs_jailhouse_dir)/interf.bin
	-cp $(SHEDLIGHT)/guests/interf-single/build/zcu104/baremetal.bin $(rootfs_jailhouse_dir)/interf-single.bin
	-cp $(SHEDLIGHT)/guests/irqstorm/build/zcu104/baremetal.bin $(rootfs_jailhouse_dir)/irqstorm.bin
	-cp $(SHEDLIGHT)/guests/ipi/build/zcu104/baremetal.bin $(rootfs_jailhouse_dir)/ipi.bin
	-cp $(SHEDLIGHT)/guests/comm/notif/tx/build/zcu104-JAILHOUSE/baremetal.bin $(rootfs_jailhouse_dir)/notif-tx.bin
	-cp $(SHEDLIGHT)/guests/comm/notif/rx/build/zcu104-JAILHOUSE/baremetal.bin $(rootfs_jailhouse_dir)/notif-rx.bin
	-cp $(SHEDLIGHT)/guests/comm/transfer/tx/build/zcu104-JAILHOUSE/baremetal.bin $(rootfs_jailhouse_dir)/transfer-tx.bin
	-cp $(SHEDLIGHT)/guests/comm/transfer/rx/build/zcu104-JAILHOUSE/baremetal.bin $(rootfs_jailhouse_dir)/transfer-rx.bin
	-cp $(SHEDLIGHT)/guests/boot/build/zcu104/128k/baremetal.bin $(rootfs_jailhouse_dir)/boot128k.bin
	-cp $(SHEDLIGHT)/guests/boot/build/zcu104/512k/baremetal.bin $(rootfs_jailhouse_dir)/boot512k.bin
	-cp $(SHEDLIGHT)/guests/boot/build/zcu104/1024k/baremetal.bin $(rootfs_jailhouse_dir)/boot1m.bin
	-cp $(SHEDLIGHT)/guests/boot/build/zcu104/2048k/baremetal.bin $(rootfs_jailhouse_dir)/boot2m.bin
	-cp $(SHEDLIGHT)/guests/boot/build/zcu104/8192k/baremetal.bin $(rootfs_jailhouse_dir)/boot8m.bin
	-cp $(SHEDLIGHT)/guests/boot/build/zcu104/32768k/baremetal.bin $(rootfs_jailhouse_dir)/boot32m.bin
	-cp $(SHEDLIGHT)/guests/boot/build/zcu104/65536k/baremetal.bin $(rootfs_jailhouse_dir)/boot64m.bin
	cp -r $(SHEDLIGHT)/jailhouse/scripts $(rootfs_jailhouse_dir)
	-cp $(SHEDLIGHT)/jailhouse/scripts/$(CONFIG).sh $(rootfs_jailhouse_dir)/scripts/boot-script.sh
	
$(rootfs_jailhouse_dir): $(INSTALL_ROOT)
	-mkdir -p $(rootfs_jailhouse_dir)

cloc: build
	cat cloc.txt | xargs cloc --by-file-by-lang 
	cloc --by-file-by-lang jailhouse/driver/*.c jailhouse/driver/*.h
	aarch64-none-elf-size -t $(jailhouse_dir)/hypervisor/hypervisor.o
	aarch64-none-elf-size -t $(jailhouse_dir)/driver/jailhouse.ko

.PHONY: build install install-root install-cells $(install_dir) buildroot cloc clean
