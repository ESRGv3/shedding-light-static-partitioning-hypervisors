# Interrupt Latency

## Build guests

Start by compiling the guests:

```
# make -C $SHEDLIGHT/guests/irqlat
# make -C $SHEDLIGHT/guests/irqstorm
# make -C $SHEDLIGHT/guests/ipi
# make -C $SHEDLIGHT/guests/interf2
# make -C $SHEDLIGHT/guests/interf2 MEM_BASE=0x48000000
```

## Base and interferenece latency experiments (irqlat-base)

The first thing you need to do is run the baremetal benchmark without the
hypervisor. For this, copy *$SHEDLIGHT/guests/irqlat/build/zcu104/baremetal.bin*
to *$SHEDLIGHT/install/boot*, and [move its contents to the sd
card](../../README.md#install). Start the board and open both terminals. To
start the baremetal application type `run baremetal` and save the output as
described in the previous section. Save the result in
$SHEDLIGHT/experiments/irqlat/irqlat-base/baremetal.

Run these instructions for each hypervisor, for each configuration. 
These are five configurations and the respective file name under
which the results must be saved:

* **irqlat** (no $SUFFIX)
* **irqlat+interf** ($SUFFIX is +interf)
* **irqlat+col**[^1] ($SUFFIX is +col)
* **irqlat+interf+col**[^1] ($SUFFIX is +interf+col)
* **irqlat+interf+col+hypcol**[^1] ($SUFFIX is +interf+col+hypcol)

First [build the hypervisors](../../README.md#build)

Then, again, [copy the contents of the install directory to the sd
card](../../README.md#install-the-hypervisors) and start the board. Type `run $HYPERVISOR`. 
Save the results with the name according to the suffixes in the above list. For
example, for Xen running the **irqlat+interf** configuration save it as
*xen+interf*. For the base case of just **irqlat** save it as *xen*.

After running all experiments for the hypervisor/configurations you wish to 
assess, to view the resulting plots:

```
# cd $SHEDLIGHT/experiments/irqlat/irqlat-base
# ./irqlat.py
```

## Direct Interrupt injection (irqlat-di)

This experiment is only appliable to Jailhouse and Bao. To run the direct
injection experiment in Jailhouse you will need toset the `CONFIG_IRQ_PASSTHRU`
macro to 1 in $SHEDLIGHT/jailhouse/config.h (remember to set this macro back to
0 after finishing this experiment).

Repeat the procedure for the irqlat-base experiment for the following configurations,
saving the results in $SHEDLIGHT/experiments/irqlat/irqlat-di/${HYPERVISOR}${SUFFIX}:

* **irqlat+di** (no $SUFFIX)
* **irqlat+di+interf** ($SUFFIX is +interf)
* **irqlat+di+interf+col**[^1] ($SUFFIX is +interf+col)

After running all experiments for the hypervisor/configurations you wish to 
assess, to view the resulting plots:

```
# cd $SHEDLIGHT/experiments/irqlat/irqlat-di
# ./irqlat-di.py
```

## Priority Handling (irqstorm)

First you need to replace *$SHEDLIGHT/install/boot/BOOT.BIN* in by 
*$SHEDLIGHT/firmware/BOOT-INTERRUPTER.BIN* to use the firmware containing the
bitstream with the IP for triggering multiple interrupt simultaneously

```
# cp $SHEDLIGHT/firmware/BOOT-INTERRUPTER.BIN $SHEDLIGHT/install/boot/BOOT.BIN
```

Run the baremetal benchmark without the hypervisor. For this, copy
*$SHEDLIGHT/guests/irqstorm/build/zcu104/baremetal.bin* to
*$SHEDLIGHT/install/boot*, and [move its contents to the sd
card](../../README.md#install). Start the board and open both terminals. To
start the baremetal application type `run baremetal` and following the "save the
output" section steps, Save the result in $SHEDLIGHT/experiments/irqlat/irqstorm/baremetal.

Next, you just need to replicate the steps in irqlat-base for the
**irqstorm** configuration, saving the results in $SHEDLIGHT/experiments/irqlat/irqstorm/${HYPERVISOR}.

After the experiment replace the original firmware in the install directory:

```
# cp $SHEDLIGHT/firmware/BOOT.BIN $SHEDLIGHT/install/boot/BOOT.BIN
```

To generate the plots for the results:

```
# cd $SHEDLIGHT/experiments/irqlat/irstorm
# ./irqstorm.py
```

## IPI (ipi)

The first thing you need to do is run the baremetal benchmark without the hypervisor. For this, copy
*$SHEDLIGHT/guests/ipi/build/zcu104/baremetal.bin* to *$SHEDLIGHT/install/boot*, and [move its
contents to the sd card](../../README.md#install). Start the board and open both terminals. To start
the baremetal application type `run baremetal` and following the "save the output" section steps,
 Save the result in $SHEDLIGHT/experiments/irqlat/ipi/baremetal.

For this experiment you just need to replicate the steps in irqlat-base for the
**ipi** configuration, saving the results in $SHEDLIGHT/experiments/irqlat/ipi/${HYPERVISOR}.

To generate the plots for the results:

```
# cd $SHEDLIGHT/experiments/irqlat/irqlat-di
# ./ipi.py
```

## Run experiment and save the output

After you start running the interrupt latency benchmark you well see the
"Press 's' to start...." message in your terminal. Before pressing 's',
start the capture:

1. In minicom press *CTRL+A* then *L*. The output file must be saved in
$SHEDLIGHT/experiments/irqlat/$EXPERIMENT/${HYPERVISOR}${SUFFIX} where the
$SUFFIX depends on the experiment configuration. For example, for the base case
there is no suffix, so the results should be saved only under $HYPERVISOR. But
for the interference case the suffix is '+interf' so the results should be saved
under $HYPERVISOR+interf;

3. After pressing 's', the test will run. When it ends, press *CTRL+A* then *L*
and select 'Close' to save the file.

[^1]: Remember you need to [re-configure Xen for cache coloring](../../xen/README md#configure-cache-coloring).
