
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

Make sure the board is setup to boot from the SD card. Follow the **MPSoC
Device Configuration** section in the [ZCU104 Evaluation Board User
Guide](https://www.xilinx.com/support/documentation/boards_and_kits/zcu104/ug1267-zcu104-eval-bd.pdf).

# Get and build the software

----
**NOTE**

From now on we'll refer to the repo's base directory as `$SHEDLIGHT`.

----

## Setup your system

We've prepared a docker image that contains all the necessary tools to build
all hypervisors and guests and process the results. You must of course first
[install docker](), and then you can start the container by running the following
command in the repo's top-level directory:

```
docker run -v $(pwd):$(pwd) -w $(pwd) -it josecm/shedlight:latest
```

This will fetch the image from docker hub, but we still provide the Dockerfile
used to build it in *$SHEDLIGHT/docker/Dockerfile* if you wish to build it 
yourself.


## Get the prebuilt firmware

The directory '$SHEDLIGHT/firmware/2021.2-zcu104-release the pre-built boot binaries
for the zcu104. Besides the original *BOOT.BIN* it contains
*BOOT-INTERRUPT.BIN* is used for the multiple interrupt experiment as it
contains the custom IP needed for it , while *BOOT-DIRECT.BIN* is used for the
boot time experiments (it removes uneeded functionality and logging from uboot
and atf.s

## Build the guests
- [Linux](guests/linux/README.md)
- [Baremetal](guest/baremetal/README.md)

## Build the hypervisors (including privilged VMs and tools):
- [Jailhouse](jailhouse/README.md)
- [Xen](xen/README.md)
- [SeL4 Camkes VMM](sel4/README.md)
- [Bao](bao/README.md)

# Install the hypervisors

Inside the directory of each hypervisor you can run 
`make CONFIG=$TARGET_CONFIG install` and the hypervisor will be built for the
target configuration and install all necessary bnaries in *$SHEDLIGHT/install/boot*.

Jailhouse is an exception. By running `make install-root` it will install the
rootcell image in *$SHEDLIGHT/install/boot* and the root cell rootfs in *$SHEDLIGHT/install/root*.  By running `make install-cells` it will install the
guests images, dtbs and configurations in *$SHEDLIGHT/install/root*.

We must than transfer the contents of *$SHEDLIGHT/install/boot* and 
*$SHEDLIGHT/install/root* to you sdcard's boot and root partitions respectively.
This must be done for *$SHEDLIGHT/install/boot* everytime you rebuild one or more
hypervisors for a different configuration, except for Jailhouse for which we must
copy *$SHEDLIGHT/install/root* in case a guest config or image has been updated or
*$SHEDLIGHT/install/boot* in case the root cell has been updated.

## Run the Experiments
- [MiBench]()
- [Interrupt Latency]()
- [Inter-VM Comm]()
- [Boot TIme]()
- [Code Size and TCB]()
