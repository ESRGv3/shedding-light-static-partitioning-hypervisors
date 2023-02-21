# Clone the repo

First of all you need to clone this repo and its submodules:

```
git clone --recursive git@gitlab.com:ESRGv3/shedding-light-static-partitioning-hypervisors.git
```

----
**NOTE**

We assume you are using a Debian-based distribution and bash throughout this guide.

----


# Setup the SD Card

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

# Setup the board

These work targets the Xilinx ZCU104 board.
Make sure the board is setup to boot from the SD card. Follow the **MPSoC
Device Configuration** section in the [ZCU104 Evaluation Board User
Guide](https://www.xilinx.com/support/documentation/boards_and_kits/zcu104/ug1267-zcu104-eval-bd.pdf).

# Get and build the software

----
**NOTE**

From now on we'll refer to the repo's base directory as `$SHEDLIGHT`.

Also, we'll use `$HYPERVISOR` as a placeholder for any of the hypervisors 
used: `jailhouse`, `xen`, `bao`, or `sel4`.

----

## Setup your system

We've prepared a docker image that contains all the necessary tools to build
all hypervisors and guests and process the results. You must of course first
[install docker](https://docs.docker.com/engine/install/ubuntu/),
and then you can start the container by running the following command in the 
repo's top-level directory:

```
docker run -v $(pwd):$(pwd) -w $(pwd) -it josecm/shedlight:latest
```

This will fetch the image from docker hub, but we still provide the Dockerfile
used to build it in *$SHEDLIGHT/docker/Dockerfile* if you wish to build it 
yourself.


## Prebuilt firmware

The directory *$SHEDLIGHT/firmware/2021.2-zcu104-release* the pre-built boot
binaries for the zcu104. Besides the original *BOOT.BIN* it contains
*BOOT-INTERRUPT.BIN* is used for the multiple interrupt experiment as it
contains the custom IP needed for it , while *BOOT-DIRECT.BIN* is used for the
boot time experiments (it removes uneeded functionality and logging from uboot
and atf.

## Setup the hypervisors (including privilged VMs and tools):
- [Jailhouse](jailhouse/README.md)
- [Xen](xen/README.md)
- [SeL4 Camkes VMM](sel4/README.md)
- [Bao](bao/README.md)

## Install the hypervisors

Inside the directory of each hypervisor you can run `make CONFIG=$TARGET_CONFIG
install` and the hypervisor will be built for the target configuration and
install all necessary bnaries in *$SHEDLIGHT/install/boot*.

Jailhouse is an exception. By running `make install-root` it will install the
rootcell image in *$SHEDLIGHT/install/boot* and the root cell rootfs to
*$SHEDLIGHT/install/root*.  By running `make install-cells` it will install the
guests images, dtbs, configurations and run scripts to *$SHEDLIGHT/install/root*.

We must than transfer the contents of *$SHEDLIGHT/install/boot* and
*$SHEDLIGHT/install/root* to you sdcard's boot and root partitions
respectively. This must be done for *$SHEDLIGHT/install/boot* everytime you
rebuild one or more hypervisors for a different configuration, except for
Jailhouse for which we must copy *$SHEDLIGHT/install/root* in case a guest
config or image has been updated or *$SHEDLIGHT/install/boot* in case the root
cell has been updated.

## Run the Experiments

We make use of both available UARTs on the board. After plugging the board to
your machine via USB, open them simultaneously up in your preferred terminal.
They are usually available under */dev/ttyUSB1* and */dev/ttyUSB2*.

There are predefined u-boot commands to run each of the hypervisors in the provided
u-boot enviroment (*$SHEDLIGHT/install/boot/uboot.env*). To start an hypervisor
you can simply use `run $HYPERVISOR`.

You'll need to use a terminal which allows to capture the output. We recommend
minicom for which you can easily start/stop the capture by pressing 'ctrl+A' 
and then 'L'.

Read the specific instruction for you target experiment:

- [MiBench]()
- [Interrupt Latency](experiments/irqlat/README.md)
- [Inter-VM Comm]()
- [Boot Time]()
- [Code Size and TCB]()
