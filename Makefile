include setup.mk

export CONFIG

install:
	$(MAKE) -C bao install
	$(MAKE) -C jailhouse install-cells
	$(MAKE) -C xen install
	$(MAKE) -C sel4 install
