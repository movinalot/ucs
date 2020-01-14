""" Instantiate a UCS Service Profile from Template and Associate """

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.ls.LsBinding import LsBinding
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.mometa.org.OrgOrg import OrgOrg

HANDLE = UcsHandle(
    "sandbox-ucsm1.cisco.com",
    "admin",
    "password"
)

HANDLE.login()

ORG_ORG = OrgOrg(
    parent_mo_or_dn='org-root',
    name="devnet",
)
HANDLE.add_mo(ORG_ORG, modify_present=True)
HANDLE.commit()

SP_TEMPLATE = LsServer(
    parent_mo_or_dn='org-root/org-devnet',
    name="devcore_template",
    type="updating-template"
)
HANDLE.add_mo(SP_TEMPLATE, modify_present=True)
HANDLE.commit()

HANDLE.logout()
