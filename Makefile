include setup.mk

export CONFIG

install:
	$(MAKE) -C bao install NO_SUPERPAGES=$(NO_SUPERPAGES)
	$(MAKE) -C jailhouse install-cells
	$(MAKE) -C xen install
	$(MAKE) -C sel4 install

.PHONY: install
