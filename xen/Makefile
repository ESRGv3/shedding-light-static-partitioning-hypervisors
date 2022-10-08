include ../setup.mk

xen_dir:=$(SHEDLIGHT)/xen
imagebuilder:=$(xen_dir)/imagebuilder
configs:=$(xen_dir)/configs/$(CONFIG)
target:=$(xen_dir)/xen/xen/xen
devicetree_dir:=$(xen_dir)/device-tree
dtss:=$(wildcard $(devicetree_dir)/*.dts)
dtbs:=$(dtss:.dts=.dtb)

build: $(target)

$(target):
	export XEN_TARGET_ARCH=arm64 CROSS_COMPILE=aarch64-none-linux-gnu- && \
		cd $(xen_dir)/xen/xen \
		make defconfig && \
		make -j$(nproc)

install: $(target) $(dtbs)
	$(imagebuilder)/scripts/uboot-script-gen -c $(configs) \
		-d $(SHEDLIGHT) -t "fatload mmc 0" -i $(INSTALL_BOOT)

%.dtb: %.dts
	dtc $< -o $@

cloc: build
	make -C xen/xen cloc
	aarch64-none-elf-size xen/xen/xen-syms

.PHONY: build install device-tree $(target)
