# Interrupt Latency

## Build guests

Start by compiling the guests:

```
make -C $SHEDLIGHT/guests/irqlat
make -C $SHEDLIGHT/guests/irqstorm
make -C $SHEDLIGHT/guests/ipi
make -C $SHEDLIGHT/guests/interf
make -C $SHEDLIGHT/guests/interf-single
```

## Run the baremetal base case

The first thing you need to do is run the baremetal benchmark without the
hypervisor. For this, copy *$SHEDLIGHT/guests/irqlat/build/zcu104/baremetal.bin*
to *$SHEDLIGHT/install/boot*, and [move its contents to the sd
card](../../README.md#install-the-hypervisors). Start the board. To start the
baremetal application type `run baremetal`. The app will start in the second
console and propmt you to start by pressing `s`. First make sure you are
captuting the output and saving it to a file in the
*$SHEDLIGHT/experiments/irqlat-base* directory and name it *baremetal+solo*.

## Base and interferenece latency experiments

Run these instructions for each hypervisor (or the ones you target), for each
 configuration. There are five configurations:

* **irqlat**
* **irqlat+interf**
* **irqlat+col**
* **irqlat+interf+col**
* **irqlat+interf+col+hypcol**

As an example, to build the hypervisor for the **irqlat+interf** configuration,
go to the hypervisors directory *$SHEDLIGHT/$HYPERVISOR* and:

```
make CONFIG=irqlat+interf install
```

Then, again, [copy the contents of the install directory to the sd
card](../../README.md#install-the-hypervisors) and start the board. Type `run
$HYPERVISOR` and repeat the procedure described
[above](#run-the-baremetal-base-case). Save the result for each configuration
as *$HYPERVISOR+$CONFIG* in *$SHEDLIGHT/experiments/irqlat-base*, without the
name of the benchmark. For example, for Xen running the **irqlat+interf**
configuration save it as *xen+interf*. For the base case of just **irqlat**
save it as *$HYPERVISOR+solo*.

After running all experiments for the hypervisor/configurations you wish to 
assess, to view the resulting plots:

```
cd $SHEDLIGHT/experiments/irqlat-base
./irqlat.py
```

## Direct Interrupt injection

TODO

## Priority Handling

TODO

## IPI

TODO
