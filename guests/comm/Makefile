

all clean: transfer/tx transfer/rx notif/tx notif/rx

transfer/tx transfer/rx notif/tx notif/rx:
	$(MAKE) -C $@ HYP=BAO $(MAKECMDGOALS)
	$(MAKE) -C $@ HYP=XEN $(MAKECMDGOALS)
	$(MAKE) -C $@ HYP=SEL4 $(MAKECMDGOALS)
	$(MAKE) -C $@ HYP=JAILHOUSE $(MAKECMDGOALS)

.PHONY: all transfer/tx transfer/rx notif/tx notif/rx
