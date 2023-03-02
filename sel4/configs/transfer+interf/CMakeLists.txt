#
# Copyright 2018, Data61, CSIRO (ABN 41 687 119 230)
#
# SPDX-License-Identifier: BSD-2-Clause
#

cmake_minimum_required(VERSION 3.8.2)

project(camkes-vmm-zynqmp-baremetal-guest)

include(${CAMKES_ARM_VM_HELPERS_PATH})

if("${KernelARMPlatform}" STREQUAL "qemu-arm-virt")
    include(simulation)
    set(SIMULATION ON CACHE BOOL "Generate simulation script to run qemu with the proper arguments")
    if(SIMULATION)
        GenerateSimulateScript()
    endif()
endif()

AddToFileServer("tx" "../../../../../../guests/comm/transfer/tx/build/zcu104-SEL4/baremetal.bin")
AddToFileServer("rx" "../../../../../../guests/comm/transfer/rx/build/zcu104-SEL4/baremetal.bin")
AddToFileServer("interf" "../../../../../../guests/interf-single/build/zcu104@0x48000000/baremetal.bin")

AddCamkesCPPFlag(cpp_flags CONFIG_VARS VmEmmc2NoDMA VmVUSB Tk1DeviceFwd Tk1Insecure)

DefineCAmkESVMFileServer()

CAmkESAddImportPath(${KernelARMPlatform})

# Define our VM Component with out cross vm dataports glue code
DeclareCAmkESComponent(VM SOURCES src/comm_connections.c)

# Declare root server
DeclareCAmkESRootserver(
    vm_minimal.camkes
    CPP_FLAGS
    ${cpp_flags}
    CPP_INCLUDES
    ${CAMKES_VM_DIR}/components/VM_Arm
)
