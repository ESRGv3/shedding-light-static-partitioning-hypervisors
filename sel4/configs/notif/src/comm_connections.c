/*
 * Copyright 2019, Data61, CSIRO (ABN 41 687 119 230)
 *
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include <camkes.h>
#include <vmlinux.h>
#include <sel4vm/guest_vm.h>

#include <sel4vmmplatsupport/drivers/cross_vm_connection.h>
#include <sel4vmmplatsupport/drivers/pci_helper.h>
#include <pci/helper.h>

#define CONNECTION_BASE_ADDRESS 0x30000000 - 0x1000

// these are defined in the dataport's glue code
extern dataport_caps_handle_t crossvm_dp_0_handle;
extern dataport_caps_handle_t crossvm_dp_1_handle;

static struct camkes_crossvm_connection connections[] = {
    {&crossvm_dp_0_handle, signal_out_emit, -1, "conn_0"},
};

static int consume_callback(vm_t *vm, void *cookie)
{
    consume_connection_event(vm, connections[0].consume_badge, true);
    return 0;
}

extern seL4_Word signal_in_notification_badge(void);
void init_cross_vm_connections(vm_t *vm, void *cookie)
{
    connections[0].consume_badge = signal_in_notification_badge();
    int err = register_async_event_handler(connections[0].consume_badge, consume_callback, NULL);
    ZF_LOGF_IF(err, "Failed to register_async_event_handler for init_cross_vm_connections.");

    cross_vm_connections_init(vm, CONNECTION_BASE_ADDRESS, connections, ARRAY_SIZE(connections));
}

DEFINE_MODULE(cross_vm_connections, NULL, init_cross_vm_connections)
