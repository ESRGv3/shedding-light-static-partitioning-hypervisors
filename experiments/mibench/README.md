# Performance

## Build guests

First [build the linux guest, the mibench benchmark and the perf
tool](../../guests/linux/README.md). Then buil the interference guest:

```
# make -C $SHEDLIGHT/guests/interf
# make -C $SHEDLIGHT/guests/interf MEM_BASE=0x48000000
```

## Mibench

First run the native benchmark. For this copy
$SHEDLIGHT/guests/linux/lloader/linux.bin to the boot install directory
($SHEDLIGHT/install/boot) and [copy its contents to the sd
card](../../README.md#install-the-hypervisors), and [start the
board](../../README.md#start-the-board). On uboot prompt execute `run linux`.
and follow the [instructions to run the experiment and save the
output](#run-experiment-and-save-the-output) under
$SHEDLIGHT/experiments/mibench/mibench-base/baremetal.

Next, for each hypervisor, for each of the following configurations, follow the
steps:

* **mibench** (no $SUFFIX)
* **mibench+interf** ($SUFFIX is +interf)
* **mibench+col**[^1] ($SUFFIX is +col)
* **mibench+interf+col**[^1] ($SUFFIX is +interf+col)
* **mibench+interf+col+hypcol**[^1] ($SUFFIX is +interf+col+hypcol)

[Build the hypervisors](../../README.md#build). Then, [copy the contents of the
install directory to the sd card](../../README.md#install-the-hypervisors),
[start the board](../../README.md#start-the-board), and [run the
hyepervisors](../../README.md#run).

[Run the experiments and save the output](#run-experiment-and-save-the-output)
to *$SHEDLIGHT/experiments/mibench/mibench-base*.

### No Superpages

To repeat the **mibench** experiment without the use of superages follow these
steps:

1. Set `CONFIG_NO_SUPERPAGES` in $SHEDLIGHT/jailhousec/config.h to 1.
2. Enable [cache coloring for Xen](../../xen/README.md#configure-cache-coloring)
3. Rebuild each hypervisor and pass `NO_SUPERPAGES=1` as a make arguments (note
   you don't need to do it for sel4/CAmkES-VMM as it already does not support
   superpages).

And repeat the exeperiment as described previously.

To observe the plotted output:

```
# cd $SHEDLIGHT/experiments/mibench
# ./mibench.py
```

## Run experiment and save the output

After you start running the benchmark the linux guest will boot (the password
for root is 'root'). Then:

1. In minicom press *CTRL+A* then *L*. The output file must be saved in
$SHEDLIGHT/experiments/mibench-n/$EXPERIMENT/${HYPERVISOR}${SUFFIX} where the
$SUFFIX depends on the experiment configuration. For example, for the base case
there is no suffix, so the results should be saved only under $HYPERVISOR. But
for the interference case the suffix is '+interf' so the results should be saved
under $HYPERVISOR+interf;

2. Run `./mibench/run.sh`.

3. After the benchmark finishes executing press *CTRL+A* then *L* and select
close to save the file with the output.

[^1]: Remember you need to [re-configure Xen for cache
    coloring](../../xen/README.md#configure-cache-coloring).

