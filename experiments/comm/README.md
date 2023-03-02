# Inter-VM Communication

## Build guests

Start by compiling the guests:

```
# make -C $SHEDLIGHT/guests/comm
# make -C $SHEDLIGHT/guests/interf-single
# make -C $SHEDLIGHT/guests/interf-single MEM_BASE=0x48000000
```

## Inter-VM Notification Latency (notif)

Run these instructions for each hypervisor, for each configuration. 
These are five configurations:

* **notif** (no $SUFFIX)
* **notif+interf** ($SUFFIX is +interf)
* **notif+interf+col**[^1] ($SUFFIX is +interf+col)
* **notif+interf+col+hypcol**[^1] ($SUFFIX is +interf+col+hypcol)

To [build the hypervisors](../../README.md#build), [copy the contents of the
install directory to the sd card](../../README.md#copy-images-to-sd-card) and
[start the board](../../README.md#setup-and-start-the-board).

On uboot prompt execute [run the hypervisor](../../README.md#run). Then [run the
experiment and save its ouput](#run-experiment-and-save-the-output)

Save the results with the name according to the suffixes in above list. 
For example, for Xen running the **notif+interf** configuration save it as
*xen+interf*. For the base case of just **irqlat** save it as *xen*.

After running all experiments for the hypervisor/configurations you wish to 
assess, to view the resulting plots:

```
# cd $SHEDLIGHT/experiments/comm/notif
# ./notif.py
```

## Inter-VM Notification Data Transfer Throughput (transfer)

Repeat the instructions for the previous *notif* experiment using the 
configurations:

* **transfer** (no $SUFFIX)
* **transfer+interf** ($SUFFIX is +interf)

After running all experiments for the hypervisor/configurations you wish to 
assess, to view the resulting plots:

```
# cd $SHEDLIGHT/experiments/comm/notif
# ./transfer.py
```

## Run experiment and save the output

After you start running the benchmark you well see the "Press 's' to start...."
message in your terminal. Before pressing 's', start the capture:

1. In minicom press *CTRL+A* then *L*. The output file must be saved in
$SHEDLIGHT/experiments/comm/$EXPERIMENT/${HYPERVISOR}${SUFFIX} where the $SUFFIX
depends on the experiment configuration. For example, for the base case there is
no suffix, so the results should be saved only under $HYPERVISOR. But for the
interference case the suffix is '+interf' so the results should be saved under
$HYPERVISOR+interf;

2. After pressing 's', the test will run. When it ends, press *CTRL+A* then *L*
and select 'Close' to save the file.

[^1]: Remember you need to [re-configure Xen for cache coloring](../../xen/README.md#configure-cache-coloring).
