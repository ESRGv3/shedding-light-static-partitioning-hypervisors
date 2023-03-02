all: build

include ../setup.mk

bao_dir:=$(realpath bao)
configs:=$(realpath configs)
target:=$(bao_dir)/bin/zcu104/builtin-configs/$(CONFIG)/bao.bin
device_tree_dir:=$(realpath device-tree)

build: $(target)

$(target):
	make -C $(bao_dir) PLATFORM=zcu104 CONFIG_REPO=../configs CONFIG=$(CONFIG) CONFIG_BUILTIN=y NO_SUPERPAGES=$(NO_SUPERPAGES)

install: $(target)
	cp $(target) $(INSTALL_BOOT)

unexport CONFIG

cloc: build
	make -C $(bao_dir) PLATFORM=zcu104 CONFIG= all cloc
	aarch64-none-elf-size $(bao_dir)/bin/zcu104/bao.elf

.PHONY: build install $(target) cloc
