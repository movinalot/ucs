"""
vmedia_boot.py

Purpose:
    modify vmedia boot policy
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
import connection as Connection

UCS_HOST = Connection.UCS_HOST
UCS_USER = Connection.UCS_USER
UCS_PASS = Connection.UCS_PASS

HANDLE = UcsHandle(UCS_HOST, UCS_USER, UCS_PASS)
HANDLE.login()

BOOT_POLICY = LsbootVirtualMedia(
    parent_mo_or_dn="org-root/boot-policy-virt-media-add",
    access="read-only-remote-cimc",
    order="3"
)
HANDLE.add_mo(BOOT_POLICY, True)
HANDLE.commit()

# Get boot items (children) of Boot Policy
OBJECTS = HANDLE.query_children(in_dn="org-root/boot-policy-virt-media-add")

# Update boot items order
for mo in OBJECTS:
    if mo.access == "read-only-remote-cimc":
        mo.order = "1"
        print(mo)
        HANDLE.set_mo(mo)
    elif mo.access == "read-write":
        storage_object = HANDLE.query_dn(
            "org-root/boot-policy-virt-media-add/storage/local-storage/local-hdd"
        )
        storage_object.order = str(int(storage_object.order)+1)
        print(storage_object)
        HANDLE.set_mo(storage_object)
    else:
        mo.order = str(int(mo.order)+1)
        print(mo)
        HANDLE.set_mo(mo)

HANDLE.set_dump_xml()
HANDLE.commit()

HANDLE.logout()
