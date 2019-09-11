from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
import connection as Connection

UCS_HOST = Connection.UCS_HOST
UCS_USER = Connection.UCS_USER
UCS_PASS = Connection.UCS_PASS

handle = UcsHandle(UCS_HOST, UCS_USER, UCS_PASS)

handle.login()

boot_policy = LsbootVirtualMedia(parent_mo_or_dn="org-root/boot-policy-virt-media-add", access="read-only-remote-cimc", order="3")
handle.add_mo(boot_policy, True)
handle.commit()

# Get boot items (children) of Boot Policy
objects = handle.query_children(in_dn="org-root/boot-policy-virt-media-add")
 
# Update boot items order
for object in objects:
    if object.access == "read-only-remote-cimc":
        object.order = "1"
        print(object)
        handle.set_mo(object)
    elif object.access == "read-write":
       # object.order = str(int(object.order)+1)
       # print(object)
        storage_object = handle.query_dn("org-root/boot-policy-virt-media-add/storage/local-storage/local-hdd")
        storage_object.order = str(int(storage_object.order)+1)
        print(storage_object)
        handle.set_mo(storage_object)
    else:
        object.order = str(int(object.order)+1)
        print(object)
        handle.set_mo(object)
 
# Commit

handle.set_dump_xml()
handle.commit()

handle.logout()
