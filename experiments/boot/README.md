# Boot Time

Replace *BOOT.BIN* by *BOOT-DIRECT.BIN* in the *install/boot directory*. This firwmare
removes some logging overheads from the firmware and bootloader:

```
# cp $SHEDLIGHT/firmware/BOOT-DIRECT.BIN $SHEDLIGHT/install/boot/BOOT.BIN 
```

(Remember to replace the original one after finishing the experiment.)

## Boot Phases By VM Time


Start by building the guest images for the various sizes:

```
# make -C $SHEDLIGHT/guests/boot IMG_SZ_KB=128
# make -C $SHEDLIGHT/guests/boot IMG_SZ_KB=512
# make -C $SHEDLIGHT/guests/boot IMG_SZ_KB=2048
# make -C $SHEDLIGHT/guests/boot IMG_SZ_KB=8192
# make -C $SHEDLIGHT/guests/boot IMG_SZ_KB=32768
# make -C $SHEDLIGHT/guests/boot IMG_SZ_KB=65536
```

For each hypervisor follow these steps:

1. Copy the automatic boot uboot enviroment for the hypervisor to the install directory:

```
# cp firmware/uboot-$HYPERVISOR.env $SHEDLIGHT/install/boot/uboot.env
```

2. [Build the config for the target image size](../../README.md#build), and
[copy the contents of the install directories to the sd
card(../../README.md#install-the-hypervisors)]. There is a target config for
each size:

* **boot128k**
* **boot512k**
* **boot2m**
* **boot8m**
* **boot32m**
* **boot64m**

3. Setup the minicom screen capture by pressing *CTRL+A* then *L* and save it to
*$HYPERVISOR-$SIZE* in *$SHEDLIGHT/exeriments/boot/boot-imgsize*. For example for
the jailhouse hypervisor and the **boot128k** configuration save it as
jailhouse-128k.

4. Turn the board on, wait for the system to boot, then turn it off. Repeat for
the number of samples you want to collect (5-10 should be enough for reproducing
the paper's results).

5. Close the screen capture by pressing *CTRL+A* then *L* and *Close*;

6. Repeat from step 2 for each image size.

To view the results:

```
# cd $SHEDLIGHT/experiments/boot/boot-imgsize
# ./boottime.py
```

## Boot time for dual Linux/FreeRTOS configuration

Build the [linux guest](../../guests/linux/README.md) as well as freertos:

```
# make $SHEDLIGHT/guests/freertos
```

Run each native guest to get the baseline boot times. For FreeRTOS:

1. Copy the automatic boot uboot enviroment for the hypervisor to the install directory:

```
# cp firmware/uboot-freertos.env $SHEDLIGHT/install/boot/uboot.env
```

2. Copy *$SHEDLIGHT/guests/freertos/build/zcu104/freertos.bin* to *$SHEDLIGHT/install/boot*
and [copy the contents of the install directory to the sd card]((../../README.md#install-the-hypervisors)).

3. Start the board and setup the minicom screen capture for UART0 by opening a
terminal to it and pressing by pressing *CTRL+A* then *L* and save it to
*$SHEDLIGHT/exeriments/boot/boot-dual/base-freertos*.

4. Turn the board on, wait for the system to boot, then turn it off. Repeat for
the number of samples you want to collect (5-10 should be enough for reproducing
the paper's results).

5. Close the screen capture by pressing *CTRL+A* then *L* and *Close*;

For Linux:

1. Copy the automatic boot uboot enviroment for the hypervisor to the install directory:

```
# cp firmware/uboot-linux.env $SHEDLIGHT/install/boot/uboot.env
```

2. Copy $SHEDLIGHT/guests/linux/linux-boot.bin to $SHEDLIGHT/install/boot
and [copy the contents of the install directory to the sd card]((../../README.md#install-the-hypervisors)).

3. Start the board and setup the minicom screen capture for UART1 by opening a
terminal to it and pressing by pressing *CTRL+A* then *L* and save it to
*$SHEDLIGHT/exeriments/boot/boot-dual/base-linux*.

4. Turn the board on, wait for the system to boot, then turn it off. Repeat for
the number of samples you want to collect (5-10 should be enough for reproducing
the paper's results).

5. Close the screen capture by pressing *CTRL+A* then *L* and *Close*;

Then, for each hypervisor:

1. Copy the automatic boot uboot enviroment for the hypervisor to the install directory:

```
# cp firmware/uboot-$HYPERVISOR.env $SHEDLIGHT/install/boot/uboot.env
```

2. [Build the target config](../../README.md#build), and [copy the contents of the install
directories to the sd card](../../README.md#install-the-hypervisors). There is a target config for
each single and the dual setup:

* **boot-linux** ($SUFFIX is linux)
* **boot-freertos** ($SUFFIX is freertos)
* **boot-dual** ($SUFFIX is dual) [^1]

3. Setup the minicom screen capture in both uarts by pressing *CTRL+A* then *L*. For the
**boot-linux** and **boot-freertos** save the results to *$HYPERVISOR-$SUFFIX* in
*$SHEDLIGHT/exeriments/boot/boot-dual*. For the case of the **boot-dual** save both simultaneouly ti
*$SHEDLIGHT/exeriments/boot/boot-dual/$HYPERVISOR-dual-freertos* for UART1's terminal and
*$SHEDLIGHT/exeriments/boot/boot-dual/$HYPERVISOR-dual-linux* for UART2's. For example for the bao
hypervisor and the **boot-dual** configuration save it as bao-dual-freertos and bao-dual-linux;

4. Turn the board on, wait for the system to boot, then turn it off. Repeat for
the number of samples you want to collect (5-10 should be enough for reproducing
the paper's results);

5. Close the screen capture by pressing *CTRL+A* then *L* and *Close*;

6. Repeat from step 2 for each image size.

To view the results:

```
# cd $SHEDLIGHT/experiments/boot/boot-dual
# ./bootdual.py
```

[^1]: **boot-dual** is not supported for Jailhouse as this hypervisors does not
support parallel guest boots.
