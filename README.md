# Shedding Light on Static Partitioning Hypervisors

This repo contains the artifact for the RTAS23 paper "Shedding Light on Static Partitioning Hypervisors". It comprises a number of benchmarks and tests on
four hypervisors: Jailhouse, Xen, Bao and seL4's/CAmkES-VMM.

## Clone the repo
---

First of all you need to clone this repo and its submodules:

```
# git clone --recursive git@gitlab.com:ESRGv3/shedding-light-static-partitioning-hypervisors.git
```
> **NOTE**: We assume you are using a Debian-based distribution and bash throughout this guide.

## Setup the SD Card
---

Format an sd card (at least 8GB) with a boot (1GB fat) and root (rest of space,
ext4) partitions:

```
# sudo fdisk /dev/sdcard
Command (m for help): d # and accept all prompts, until there are no more partitions
Command (m for help): w
# sudo fdisk /dev/sdcard
Command (m for help): n # all default, except size (last sector) +1GB
Command (m for help): a # to make it bootable
Command (m for help): n # all default
Command (m for help): w
# sudo mkfs.fat /dev/sdcardpart1 -n boot
# sudo mkfs.ext4 -L root /dev/sdcardpart2 
```

From now on, we'll refer to the sd card's boot partition mount point as
`$SDCARD_BOOT` and to the root partition mount point as `$SDCARD_ROOT`.


## Setup your system
---

We've prepared a docker image that contains all the necessary tools to build
all hypervisors and guests and process the results. You must of course first
[install docker](https://docs.docker.com/engine/install/ubuntu/),
and then you can start the container by running the following command in the 
repo's top-level directory:

```
# docker run -v $(pwd):$(pwd) -w $(pwd) -it josecm/shedlight:latest
```

This will fetch the image from docker hub, but we still provide the Dockerfile
used to build it in *$SHEDLIGHT/docker/Dockerfile* if you wish to build it 
yourself.

Run all build commands from this container.

> **NOTE**
> From now on we'll refer to the repo's base directory as `$SHEDLIGHT`. Also,
> we'll use `$HYPERVISOR` as a placeholder for any of the hypervisors used:
> `jailhouse`, `xen`, `bao`, or `sel4`; and `$CONFIG` to signify the target
> configuration for which we want to build the hypervisor. For example, the
> interrupt latency experiments are under the `irqlat` config. Each experiment's
> README file details the name of the configurations used.

## Hypervisors
---

### Setup

You will need to manually [build the Jailhouse's root
cell](jailhouse/README.md#build-root-cell).

### Build

We provide Makefiles that automate the build process for the hypervisors. But
we also provide step-by-step instructions on how you can do this by hand:

- [Jailhouse](jailhouse/README.md)
- [Xen](xen/README.md)
- [SeL4 Camkes VMM](sel4/README.md)[^1]
- [Bao](bao/README.md)

Inside the directory of each hypervisor, you can run `make install
CONFIG=$CONFIG` and the hypervisor will be built for the target configuration
and install all necessary binaries in *$SHEDLIGHT/install/boot*. As an example,
to build the hypervisor for the **irqlat+interf** configuration, go to the
hypervisors directory *$SHEDLIGHT/$HYPERVISOR* and:

```
# make CONFIG=irqlat+interf install
```

Again Jailhouse is an exception. We distinguish between install the hypervisor
and root cell, and the rootfs containing the other guest's images. When
installing Jailhouse to the SD you can: - run `make install-root` it will
install the rootcell image in *$SHEDLIGHT/install/boot* and the root cell rootfs
to *$SHEDLIGHT/install/root*; - run `make install-cells CONFIG=$CONFIG` it will
install the guests images, dtbs, configurations and run scripts to
*$SHEDLIGHT/install/root*.

You can also build all hypervisors using a single command by running:

```
# make -C $SHEDLIGHT install CONFIG=$CONFIG
```

### Copy images to sd card

After building the hypervisors, you must than transfer the contents of
*$SHEDLIGHT/install/boot* and *$SHEDLIGHT/install/root* to you sdcard's boot and
root partitions respectively:

```
# cp -r install/boot/* $SDCARD_BOOT
# sudo cp -r install/root/* $SDCARD_ROOT 
```

This must be done for for the boot directory everytime you rebuild one or more
hypervisors for a different configuration. Again, Jailhouse is the exception:
you must copy *$SHEDLIGHT/install/root* in case a guest config or image has been
updated, and *$SHEDLIGHT/install/boot* in case the hypervisor or root cell has
been updated (e.g. you changed *jailhouse/config.h*).

### Run

After you turn on the board and U-boot boots, running `run $HYPERVISOR` should
boot the target hypervisor. Follow the [specific instructions for each
experiment](#setup-and-run-the-experiments) detailed next to understand the
particularities of each one.

For Jailhouse, after the root cell boots (root password is root), 
you will need to run the script to initialize the other cells and start
the experiments:

```
# ./jailhouse/scripts/$CONFIG.sh
```

## Start the board
---

These work targets the Xilinx ZCU104 board. Make sure the board is setup to boot
from the SD card. Follow the **MPSoC Device Configuration** section in the
[ZCU104 Evaluation Board User
Guide](https://www.xilinx.com/support/documentation/boards_and_kits/zcu104/ug1267-zcu104-eval-bd.pdf).

We make use of both available UARTs on the board. After plugging the board to
your machine via USB, open them simultaneously up in your preferred terminal.
They are usually available under */dev/ttyUSB1* and */dev/ttyUSB2*.

Then start the board insert the SD card in the board's SD card slot and turn the power on.

> **Note** The chosen terminal program needs to have a capture functionality as
we will need it to save the results of the experiments. For this we suggest
minicom for which you can easily start/stop the capture by pressing 'ctrl+A'
and then 'L'. In our instructios we assume you are using minicom.

## Setup and run the experiments
---

Read the specific instruction for you target experiment:

- [Performance w/ MiBench](experiments/mibench/README.md)
- [Interrupt Latency](experiments/irqlat/README.md)
- [Inter-VM Comm](experiments/comm/README.md)
- [Boot Time](experiments/boot/README.md)
- [Code Size and TCB](experiments/loc/README.md)

> **NOTE**
>
> The directory *$SHEDLIGHT/firmware/2021.2-zcu104-release* contains three
> versions of pre-built boot binaries for the zcu104:
> 
> - *BOOT.BIN* is the original firmware provided by Xilinx;
> - *BOOT-INTERRUPT.BIN* is used for the irqstorm experiment as it contains the
>   bitstream with the custom IP needed for triggering multiple interrupts
>   simultaneously;
> - is used for the boot time experiments. It contains modified
>   versions of the firmware (atf) and bootloader (u-boot) that remove uneeded
>   functionality and logging.
> 
> In the *irqstorm* and *boot* experiments you will need to replace the
> $SDCARD_BOOT/BOOT.BIN by *BOOT-INTERRUPT.BIN* and *BOOT-DIRECT.BIN* ,
> respectively, and restore the original *BOOT.BIN* after those experiments 
> are done.

[^1]: The first time you build seL4/CAmkES-VMM in the docker container in may
take a while. Please be patient and wait a few minutes.
