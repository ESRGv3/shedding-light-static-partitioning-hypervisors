include ../setup.mk

xen_dir:=$(SHEDLIGHT)/xen
imagebuilder:=$(xen_dir)/imagebuilder
configs:=$(xen_dir)/configs/$(CONFIG)
target:=$(xen_dir)/xen/xen/xen
xen_config:=$(xen_dir)/xen/xen/.config
devicetree_dir:=$(xen_dir)/device-tree
dtss:=$(wildcard $(devicetree_dir)/*.dts)
dtbs:=$(dtss:.dts=.dtb)
xen_env:=XEN_TARGET_ARCH=arm64 CROSS_COMPILE=aarch64-none-linux-gnu-

build: $(target)

$(xen_config): $(xen_dir)/xen-minimal-config
	cp $< $@
	$(xen_env) make -C $(dir $(xen_config)) oldconfig

$(target): | $(xen_config)
	$(xen_env) make -C $(xen_dir)/xen/xen -j$(nproc)

install: $(target) $(dtbs)
	$(imagebuilder)/scripts/uboot-script-gen -c $(configs) \
		-d $(SHEDLIGHT) -t "fatload mmc 0" -i $(INSTALL_BOOT)

%.dtb: %.dts
	dtc $< -o $@

cloc: build
	make -C xen/xen cloc
	aarch64-none-elf-size xen/xen/xen-syms

.PHONY: build install device-tree $(target)
