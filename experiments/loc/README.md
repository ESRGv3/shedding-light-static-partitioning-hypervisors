# Code Base Size

Each hypervisor's build system provided a `cloc` make rule to measure the source
lines of code (SLoC) using the cloc tool. We need to provide a given
configuration to measure against. We can use any configruation and the results
will be essentially identical. For example, for the **mibench** config, 
for ecach hypervisor do:

```
# cd $SHEDLIGHT/$HYPERVISOR
# make cloc CONFIG=mibench
```
