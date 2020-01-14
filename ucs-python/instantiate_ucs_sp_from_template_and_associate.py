""" Instantiate a UCS Service Profile from template and associate """

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.ls.LsBinding import LsBinding
from ucsmsdk.mometa.ls.LsServer import LsServer

HANDLE = UcsHandle(
    "sandbox-ucsm1.cisco.com",
    "admin",
    "password"
)

HANDLE.login()

SP_FROM_TEMPLATE = LsServer(
    parent_mo_or_dn='org-root/org-devnet',
    name="devcore-server-01",
    src_templ_name="devcore_template",
    type="instance"
)

LsBinding(
    parent_mo_or_dn=SP_FROM_TEMPLATE,
    pn_dn="sys/chassis-7/blade-3"
)

HANDLE.add_mo(SP_FROM_TEMPLATE, modify_present=True)
HANDLE.commit()

HANDLE.logout()
