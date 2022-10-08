dir_list = $(patsubst %/,%,$(dir $(wildcard $(1)/*/.)))

SUITES:=automotive network security telecomm
benchmarks:=$(foreach suite,$(SUITES),$(wildcard $(suite)/*/Makefile) $(wildcard $(suite)/*/src/Makefile))
benchmarks:=$(dir $(benchmarks))
INSTALL_DIR:=_install
INSTALL_DIR:=$(abspath $(INSTALL_DIR))


all clean install: $(benchmarks)

$(benchmarks):
	$(MAKE) -C $@ $(MAKECMDGOALS) INSTALL_DIR=$(INSTALL_DIR)/$@

install: | $(INSTALL_DIR)
	cp ./runme.sh $(INSTALL_DIR)

$(INSTALL_DIR):
	mkdir -p $@

.PHONY: all $(benchmarks)
