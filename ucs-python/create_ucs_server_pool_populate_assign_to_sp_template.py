""" Create UCS Server Pool and associate to template """

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.compute.ComputePool import ComputePool
from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot
from ucsmsdk.mometa.ls.LsRequirement import LsRequirement

HANDLE = UcsHandle(
    "sandbox-ucsm1.cisco.com",
    "admin",
    "password"
)
HANDLE.login()

SERVER_POOL = ComputePool(
    parent_mo_or_dn="org-root/org-devnet",
    name="devcore_pool"
)
HANDLE.add_mo(SERVER_POOL, modify_present=True)

for blade in HANDLE.query_classid(
    "computeBlade",
    filter_str='(chassis_id, "7")'
    ):
    SERVER = ComputePooledSlot(
        parent_mo_or_dn=SERVER_POOL,
        chassis_id=blade.chassis_id,
        slot_id=blade.slot_id
    )
    HANDLE.add_mo(SERVER, modify_present=True)
HANDLE.commit()

SP_TEMPLATE = LsRequirement(
    parent_mo_or_dn="org-root/org-devnet/ls-devcore_template",
    name="devcore_pool"
)
HANDLE.add_mo(SP_TEMPLATE, modify_present=True)
HANDLE.commit()

HANDLE.logout()
