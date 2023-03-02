include ../setup.mk

sel4_dir:=$(realpath .)
configs:=$(sel4_dir)/configs

build_dir:=$(sel4_dir)/camkes-vmm/build-$(CONFIG)
target:=$(build_dir)/images/capdl-loader-image-arm-zynqmp

init-build_cmd:=../init-build.sh -DCAMKES_VM_APP=$(CONFIG) -DPLATFORM=zynqmp \
	-DCROSS_COMPILER_PREFIX=aarch64-none-linux-gnu- \
	-DElfloaderImage=ElfloaderImageBinary \
	-DNUM_NODES=4 \
	-DKernelArmExportPCNTUser=1 \
	-DKernelArmExportVCNTUser=1 \
	-DKernelArmExportPTMRUser=1 \
	-DKernelArmExportVTMRUser=1 \
	-DKernelArmVtimerUpdateVOffset=0 \
	-DKernelTimerTickMS=60000 \
	-DCONFIG_REPO=$(shell realpath $(configs))

# ifneq ($(filter cloc%,$(MAKECMDGOALS)),)
# $(error cloc!!)
# endif

all: build
build: $(target)

$(target): | $(build_dir)
	cd $(build_dir) && $(init-build_cmd) && ninja

$(build_dir):
	mkdir -p $@

install: $(target)
	cp $(target) $(INSTALL_BOOT)

cloc: cloc-kernel cloc-vmm
	aarch64-none-elf-size camkes-vmm/build-$(CONFIG)/kernel/kernel.elf
	aarch64-none-elf-size camkes-vmm/build-$(CONFIG)/vm0.instance.bin

ignore_platforms:

cloc-vmm: build
	aarch64-none-linux-gnu-readelf --string-dump=.debug_line_str camkes-vmm/build-$(CONFIG)/vm0.instance.bin | grep -o '\S*\.c' | grep -v libgcc | sort | uniq >  camkes-vmm/build-$(CONFIG)/vmm_srcs.txt
	cat camkes-vmm/build-$(CONFIG)/vmm_srcs.txt | xargs cat |  grep -oP '#include.*\.h' | grep -o '\S*\.h' | grep -o '[^<>"]*' |  \
		xargs -L 1 -I {} find $(sel4_dir)/camkes-vmm -wholename \*{} | sort | uniq | \
		grep -v '.*\(x86\|ia32\|mips\|power\|riscv\|aarch32\|elf32\|exynos\|odroid\|tk1\|tx1\|qemu\|tx2\|muslibc\|libgcc\|plat_include\).*' >  camkes-vmm/build-$(CONFIG)/vmm_headers.txt
	cat $(sel4_dir)/camkes-vmm/build-$(CONFIG)/vmm_srcs.txt  $(sel4_dir)/camkes-vmm/build-$(CONFIG)/vmm_headers.txt | xargs cloc --by-file-by-lang


cloc-kernel: build
	cloc --by-file-by-lang \
		camkes-vmm/build-$(CONFIG)/kernel/kernel_all_pp_prune.c \
		camkes-vmm/kernel/src/arch/arm/64/head.S \
		camkes-vmm/kernel/src/arch/arm/64/traps.S



.PHONY: build install $(target)
