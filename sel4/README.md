# seL4 Camkes VMM

# Build
    
```
# cd $SHEDLIGHT/sel4
# mkdir -p camkes-vmm/build-$CONFIG
# cd camkes-vmm/build-$CONFIG
# ../init-build.sh -DCAMKES_VM_APP=$CONFIG -DPLATFORM=zynqmp \	
    -DCROSS_COMPILER_PREFIX=aarch64-none-linux-gnu- \
	-DElfloaderImage=ElfloaderImageBinary \
	-DNUM_NODES=4 \
	-DKernelArmExportPCNTUser=1 \
	-DKernelArmExportVCNTUser=1 \	
	-DKernelArmExportPTMRUser=1 \
	-DKernelArmExportVTMRUser=1 \
    -DKernelArmVtimerUpdateVOffset=0 \
	-DKernelTimerTickMS=60000 \
    -DCONFIG_REPO= $SHEDLIGHT/sel4/configs
# ninja
# cp capdl-loader-image-arm-zynqmp $SHEDLIGHT/install/boot
```
## Install

Copy all files $SHEDLIGHT/install/boot to your $SDCARD_BOOT.

```
# cp $SHEDLIGHT/install/boot/* $SDCARD_BOOT
```

## Run

Use uboot to load the images and start the kernel:

```
fatload mmc 0 0x400000 capdl-loader-image-arm-zynqmp && go 0x400000
```



